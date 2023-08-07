import imp
import json
import datetime
from datetime import date, datetime, timedelta
from django.db.models import Sum
from django.http import Http404
from django.http import JsonResponse 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django_filters.views import FilterView
from django.views.decorators.http import require_http_methods

from .filters import SaplingActualFilter, SeedActualFilter, SproutActualFilter, PrepairLandActualFilter, \
    TreeGroundPlantingActualFilter
from .forms import *
from .models import *
from ..accounts.forms import FilterForm
from ..accounts.models import Department, Region, User, UserDepartment
from ..chorvachilik.models import ChorvachilikTypes, Chorvachilik, Animal, ChorvaInputOutputCategory, ChorvachilikActual
from django.views.generic import ListView
from .serializers import TreeHeightDepartmentSerializer

from ..core.service import get_current_user_regions_and_departments_json, get_current_user_regions_and_departments_qs
from ..finance.views import generate_month_year, _calculate_percentage, _check_sum_is_none
from ..report.models import Report as Rp
epoch_year = date.today().year
year_start = date(epoch_year, 1, 1)
year_end = date(epoch_year, 12, 31)


class JsonData:
    def get_json_data(self, department=False, region=False, tree_plant=False, tree_type=None,
                      chorvachilik_type=None, chorvachilik=None, animal=None, in_out_category=None):
        if department:
            return serialize('json', Department.objects.filter(status=1).order_by('sort'))
        elif region:
            return serialize('json', Region.objects.filter(status=1).order_by('sort'))
        elif tree_plant:
            return serialize('json', TreePlant.objects.exclude(status=2))
        elif tree_type:
            return serialize('json', TreeTypes.objects.filter(status=1))
        elif chorvachilik_type:
            return serialize('json', ChorvachilikTypes.objects.exclude(status=2))
        elif chorvachilik:
            return serialize('json', Chorvachilik.objects.filter(status=1))
        elif animal:
            return serialize("json", Animal.objects.filter(status=1))
        elif in_out_category:
            return serialize("json", ChorvaInputOutputCategory.objects.filter(status=1))
        else:
            return None


# TREE TYPES
class TreeTypeList(LoginRequiredMixin, ListView):
    template_name = 'urmon_barpo/trees/type/list.html'
    paginate_by = 10
    model = TreeTypes

    def get_context_data(self, *args, **kwargs):
        context = super(TreeTypeList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return TreeTypes.objects.exclude(status=2).order_by('-id')


class TreeTypeCreate(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/register"""
    template_name = 'urmon_barpo/trees/type/create.html'

    def get(self, request):
        try:
            form = TreeTypeForm()
            context = {
                "is_user": True, "form": form,
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request):
        try:
            form = TreeTypeForm(data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:tree_type_list')
            else:
                return redirect('trees:tree_type_list')
        except ObjectDoesNotExist:
            return redirect('trees:tree_type_list')


class TreeTypeDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/trees/type/list.html'

    def get(self, request, pk):
        qs = TreeTypes.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:tree_type_list')
        else:
            return redirect('trees:tree_type_list')


class TreeTypeDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/trees/type/detail.html'

    def get(self, request, pk):
        try:
            type = TreeTypes.objects.get(pk=pk)
            form = TreeTypeForm(initial={
                'name': type.name,
                "show_profit": type.show_profit
            })
            context = {
                "is_user": True,
                'form': form,
                "type": type
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            tree = TreeTypes.objects.get(pk=pk)
            form = TreeTypeForm(instance=tree, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:tree_type_list')
            else:
                return redirect('trees:tree_type_list')
        except ObjectDoesNotExist:
            return redirect('trees:tree_type_list')


# TREE
class TreesDashboard(LoginRequiredMixin, View):
    template_name = "urmon_barpo/dashboard.html"

    def get(self, request):
        data = Rp.objects.filter(type=2, status=1)
        context = {"data": data, "current_year": date.today().year}
        return render(request, self.template_name, context)


class TreeActionDashboard(LoginRequiredMixin, View):
    template_name = "urmon_barpo/trees/dashboard.html"

    def get(self, request):
        return render(request, self.template_name)


class TreePlantList(LoginRequiredMixin, ListView):
    template_name = 'urmon_barpo/trees/plant/list.html'
    paginate_by = 10
    model = TreePlant

    def get_context_data(self, *args, **kwargs):
        context = super(TreePlantList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return TreePlant.objects.exclude(status=2).order_by('-id')


class TreePlantCreate(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/register"""
    template_name = 'urmon_barpo/trees/plant/create.html'

    def get(self, request):
        try:
            form = TreePlantForm()
            context = {
                "is_user": True, "form": form,
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request):
        try:
            form = TreePlantForm(data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:name_list')
            else:
                return redirect('trees:name_list')
        except ObjectDoesNotExist:
            return redirect('trees:name_list')


class TreePlantDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/trees/plant/detail.html'

    def get(self, request, pk):
        try:
            tree_plan = TreePlant.objects.get(pk=pk)
            form = TreePlantForm(initial={
                'name': tree_plan.name,
                "description": tree_plan.description,
                "category": tree_plan.category,
                "is_show_sprouting:": tree_plan.is_show_sprouting,
                "is_show_seed": tree_plan.is_show_seed,
                "is_show_sapling": tree_plan.is_show_sapling,
                "is_show_height": tree_plan.is_show_height
            })
            context = {
                "is_user": True,
                'form': form,
                "tree": tree_plan
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            tree = TreePlant.objects.get(pk=pk)
            form = TreePlantForm(instance=tree, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:name_list')
            else:
                print(form.errors)
                return redirect('trees:name_list')
        except ObjectDoesNotExist:
            return redirect('trees:name_list')


class TreePlantDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/trees/plant/list.html'

    def get(self, request, pk):
        qs = TreePlant.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:name_list')
        else:
            return redirect('trees:name_list')

# TREE HEIGHT DEPARTMENT INFO
@require_http_methods(["GET"])
def get_tree_height_by_department(request, pk):
    resp = dict()
    if (request.user.is_authenticated):
        try:
            department_info = TreeHeightReport.objects.filter(department=pk).exclude(status="2")
        except Exception as e:
            print(e)
            return Http404()
        
        serializer = TreeHeightDepartmentSerializer(department_info, many=True)
        data = serializer.data

        def merge(obj1, obj2):
            fields = ["height_0_0_2_count", "height_0_2_5_count", "height_0_5_1_count", 
                    "height_1_1_5_count", "height_1_5_2_count", "height_2_count"]
            for i in fields:
                if obj2[i] is not None:
                    if obj1[i] != None:
                        obj1[i] += obj2[i]
                    else:
                        obj1[i] = obj2[i]

        for item in data:
            tree_plan = item['tree_plan']
            res_i = resp.get(tree_plan, None)
            
            if res_i == None:
                resp[tree_plan] = item
            else:
                merge(resp[tree_plan], item)

        return JsonResponse(resp, safe=False) 


# TREE HEIGHT
class TreeHeightReportList(LoginRequiredMixin, ListView):
    template_name = 'urmon_barpo/trees/tree_plan_list.html'
    paginate_by = 10
    model = TreeHeightReport

    def get_context_data(self, *args, **kwargs):
        context = super(TreeHeightReportList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return TreeHeightReport.objects.filter(region__in=regions, department__in=departments, status=1).order_by(
                '-id')
        else:
            return TreeHeightReport.objects.filter(status=44).order_by('-id')


class TreeHeightCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/trees/tree_height_create.html'

    def get(self, request):
        try:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            form = TreeHeightForm()
            context = {
                "is_user": True, "departments": departments,
                "regions": regions,
                "tree": serialize('json', TreePlant.objects.filter(is_show_height=True).order_by('sort'))
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request):
        data = request.POST
        items = json.loads(data['items'])
        if items:
            for i in range(len(items)):
                if items[i]['first'] or items[i]['second'] or items[i]['three'] or items[i]['four'] or items[i][
                    'five'] or items[i]['six']:
                    TreeHeightReport.objects.create(
                        tree_plan=TreePlant.objects.filter(id=items[i]['id']).first(),
                        height_0_0_2_count=items[i]['first'],
                        height_0_2_5_count=items[i]['second'],
                        height_0_5_1_count=items[i]['three'],
                        height_1_1_5_count=items[i]['four'],
                        height_1_5_2_count=items[i]['five'],
                        height_2_count=items[i]['six'],
                        date=data['date'],
                        region=Region.objects.get(id=data['region']),
                        department=Department.objects.get(id=data['department'])
                    )
                else:
                    continue
            return redirect('trees:tree_list')
        else:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            ctx = {"departments": departments, "regions": regions,
                   "tree": serialize('json', TreePlant.objects.filter(is_show_height=True))
                   }
            return render(request, self.template_name, ctx)


class TreeHeightReportDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/trees/tree_plan_detail.html'

    def get(self, request, pk):
        try:
            tree = TreeHeightReport.objects.get(pk=pk)
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            form = TreeHeightForm(initial={
                'tree_plan': tree.tree_plan,
                "height_0_0_2_count": tree.height_0_0_2_count,
                "height_0_2_5_count": tree.height_0_2_5_count,
                "height_0_5_1_count": tree.height_0_5_1_count,
                "height_1_1_5_count": tree.height_1_1_5_count,
                "height_1_5_2_count": tree.height_1_5_2_count,
                "date": tree.date,
                "region": tree.region,
                "department": tree.department
            })
            context = {
                "is_user": True,
                'form': form,
                "department": departments,
                "region": regions,
                "tree": tree
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            tree = TreeHeightReport.objects.get(pk=pk)
            form = TreeHeightForm(instance=tree, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:tree_list')
            else:
                return redirect('trees:tree_list')
        except ObjectDoesNotExist:
            return redirect('trees:tree_list')


class TreeHeightReportDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/trees/tree_plan_list.html'

    def get(self, request, pk):
        qs = TreeHeightReport.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:tree_list')
        else:
            return redirect('trees:tree_list')


# TREE CONTRACT
class TreeContractList(LoginRequiredMixin, ListView):
    template_name = 'urmon_barpo/tree_contract/actual/list.html'
    paginate_by = 15
    model = TreeContract

    def get_context_data(self, *args, **kwargs):
        context = super(TreeContractList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return TreeContract.objects.filter(region__in=regions, department__in=departments, status=1).order_by(
                '-id')
        else:
            return TreeContract.objects.filter(status=44).order_by('-id')


class TreeContactCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/tree_contract/actual/create.html'

    def get(self, request):
        try:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True, "departments": departments,
                "regions": regions, "contract": serialize('json', TreeContractCategory.objects.filter(status=1))
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request):
        data = request.POST
        items = json.loads(data['items'])
        if items:
            for i in range(len(items)):
                TreeContract.objects.create(
                    date=data['date'],
                    category=TreeContractCategory.objects.filter(id=items[i]['category']).first(),
                    count=items[i]['count'],
                    amount=items[i]['amount'],
                    payout=items[i]['payout'],
                    output_tree=items[i]['output_tree'],
                    region=Region.objects.get(id=data['region']),
                    department=Department.objects.get(id=data['department']),
                    creator=self.request.user
                )
            return redirect('trees:tree_contract_list')
        else:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            ctx = {"departments": departments, "regions": regions,
                   "tree_contract": serialize('json', TreeContractCategory.objects.filter(status=1))
                   }
            return render(request, self.template_name, ctx)


class TreeContractDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/tree_contract/actual/detail.html'

    def get(self, request, pk):
        try:
            tree = TreeContract.objects.get(pk=pk)
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            form = TreeContractForm(initial={
                'category': tree.category,
                "count": tree.count,
                "amount": tree.amount,
                "payout": tree.payout,
                "output_tree": tree.output_tree,
                "date": tree.date,
                "region": tree.region,
                "department": tree.department
            })
            context = {
                "is_user": True,
                'form': form,
                "department": departments,
                "region": regions,
                "tree": tree
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            tree = TreeContract.objects.get(pk=pk)
            form = TreeContractForm(instance=tree, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:tree_contract_list')
            else:
                return redirect('trees:tree_contract_list')
        except ObjectDoesNotExist:
            return redirect('trees:tree_contract_list')


class TreeContractDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/tree_contract/actual/list.html'

    def get(self, request, pk):
        qs = TreeContract.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:tree_contract_list')
        else:
            return redirect('trees:tree_contract_list')


# TREE CONTRACTPLAN
class TreeContractPlanList(LoginRequiredMixin, ListView):
    template_name = 'urmon_barpo/tree_contract/plan/list.html'
    paginate_by = 15
    model = TreeContractPlan

    def get_context_data(self, *args, **kwargs):
        context = super(TreeContractPlanList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return TreeContractPlan.objects.filter(
                region__in=regions, department__in=departments, status=1).order_by('-id')
        else:
            return TreeContractPlan.objects.filter(status=44).order_by('-id')


class TreeContactPlanCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/tree_contract/plan/create.html'

    def get(self, request):
        try:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {"is_user": True, "departments": departments, "regions": regions}
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request):
        data = request.POST
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        context = {"is_user": True, "departments": departments, "regions": regions}
        if data:
            today = datetime.today()
            check = TreeContractPlan.objects.filter(date__year=today.year, status=1, department=data['department'])
            if check.exists():
                return render(request, self.template_name, context, status=200)
            else:
                TreeContractPlan.objects.create(
                    date=today,
                    tree_count=data['tree_count'],
                    region=Region.objects.get(id=data['region']),
                    department=Department.objects.get(id=data['department']),
                    creator=self.request.user
                )
            return redirect('trees:tree_contract_plan_list')
        else:
            return render(request, self.template_name, context, status=400)


class TreeContractPlanDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/tree_contract/plan/detail.html'

    def get(self, request, pk):
        try:
            tree = TreeContractPlan.objects.get(pk=pk)
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            form = TreeContractPlanForm(initial={
                "tree_count": tree.tree_count,
                "region": tree.region,
                "date": tree.date,
                "department": tree.department
            })
            context = {
                "is_user": True,
                'form': form,
                "department": departments,
                "region": regions,
                "tree": tree
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            tree = TreeContractPlan.objects.get(pk=pk)
            form = TreeContractPlanForm(instance=tree, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:tree_contract_plan_list')
            else:
                return redirect('trees:tree_contract_plan_list')
        except ObjectDoesNotExist:
            return redirect('trees:tree_contract_plan_list')


class TreeContractPlanDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/tree_contract/plan/list.html'

    def get(self, request, pk):
        qs = TreeContractPlan.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:tree_contract_plan_list')
        else:
            return redirect('trees:tree_contract_plan_list')


class TreeContractActionDashboard(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/tree_contract/dashboard.html'

    def get(self, request):
        return render(request, self.template_name)


class TreeContractReport(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/tree_contract/reports/region_and_departments.html'

    def get(self, request):
        current_year = date.today().year
        start = date(current_year, 1, 1).strftime('%Y-%m-%d')
        end_date = date(current_year, 12, 31).strftime('%Y-%m-%d')
        end = self.request.GET.get('end', None)
        if not end:
            end_dateformat = datetime.strptime(end_date, '%Y-%m-%d')
            current_month = end_dateformat.month
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.strptime(end, '%Y-%m-%d')
            current_month = end_dateformat.month
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = end_dateformat.strftime('%Y-%m-%d')

        form = FilterForm(initial={"start": start, "end": end})
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            plan_data = TreeContractPlan.objects.filter(region__in=regions, department__in=departments,
                                                        date__year=current_year, status=1)
            actual_data = TreeContract.objects.filter(region__in=regions, department__in=departments,
                                                      date__range=[start, end], status=1)
            region_id = None,
            region_obj = None
            data = []
            x = 1
            for depart in departments:
                x = x + 1
                # PRODUCTION
                depart_plan_query = plan_data.filter(department=depart).aggregate(Sum('tree_count'))
                depart_count_query = actual_data.filter(department=depart).aggregate(Sum('count'))
                depart_amount_query = actual_data.filter(department=depart).aggregate(Sum('amount'))
                depart_payout_query = actual_data.filter(department=depart).aggregate(Sum('payout'))
                depart_output_query = actual_data.filter(department=depart).aggregate(Sum('output_tree'))

                depart_count = _check_sum_is_none(depart_count_query['count__sum'])
                depart_amount = _check_sum_is_none(depart_amount_query['amount__sum'])
                depart_payout = _check_sum_is_none(depart_payout_query['payout__sum'])
                depart_output = _check_sum_is_none(depart_output_query['output_tree__sum'])
                depart_plan = _check_sum_is_none(depart_plan_query['tree_count__sum'])

                # PAID SERVICE
                if region_id != depart.region_id:
                    # PRODUCTION
                    region_obj = Region.objects.get(id=depart.region_id)
                    region_plan_query = plan_data.filter(region=region_obj).aggregate(Sum('tree_count'))
                    region_count_query = actual_data.filter(region=region_obj).aggregate(Sum('count'))
                    region_amount_query = actual_data.filter(region=region_obj).aggregate(Sum('amount'))
                    region_payout_query = actual_data.filter(region=region_obj).aggregate(Sum('payout'))
                    region_output_query = actual_data.filter(region=region_obj).aggregate(Sum('output_tree'))

                    region_count = _check_sum_is_none(region_count_query['count__sum'])
                    region_amount = _check_sum_is_none(region_amount_query['amount__sum'])
                    region_payout = _check_sum_is_none(region_payout_query['payout__sum'])
                    region_output = _check_sum_is_none(region_output_query['output_tree__sum'])
                    region_plan = _check_sum_is_none(region_plan_query['tree_count__sum'])

                    data.append({
                        "index": 1,
                        "region_id": region_obj.id,
                        "region_plan": region_plan,
                        "region_name": region_obj.name,
                        "region_count": region_count,
                        "region_amount": region_amount,
                        "region_payout": region_payout,
                        "region_output": region_output,

                        "depart_name": depart.name,
                        "depart_id": depart.id,
                        "depart_plan": depart_plan,
                        "depart_count": depart_count,
                        "depart_amount": depart_amount,
                        "depart_payout": depart_payout,
                        "depart_output": depart_output
                    })
                    x = 1
                else:
                    data.append({
                        "index": x,
                        "depart_id": depart.id,
                        "depart_name": depart.name,
                        "depart_count": depart_count,
                        "depart_amount": depart_amount,
                        "depart_payout": depart_payout,
                        "depart_output": depart_output,
                        "depart_plan": depart_plan
                    })
                region_obj = None
                region_id = depart.region_id
            all_plan_query = TreeContractPlan.objects.filter(region__in=regions, date__year=current_year,
                                                             status=1).aggregate(
                Sum('tree_count'))
            all_count_query = TreeContract.objects.filter(region__in=regions, status=1,
                                                          date__year=current_year).aggregate(Sum('count'))
            all_amount_query = TreeContract.objects.filter(region__in=regions, status=1,
                                                           date__year=current_year).aggregate(Sum('amount'))
            all_payout_query = TreeContract.objects.filter(region__in=regions, status=1,
                                                           date__year=current_year).aggregate(Sum('payout'))
            all_output_query = TreeContract.objects.filter(region__in=regions, status=1,
                                                           date__year=current_year).aggregate(
                Sum('output_tree'))

            all_plan = _check_sum_is_none(all_plan_query['tree_count__sum'])
            all_count = _check_sum_is_none(all_count_query['count__sum'])
            all_amount = _check_sum_is_none(all_amount_query['amount__sum'])
            all_payout = _check_sum_is_none(all_payout_query['payout__sum'])
            all_output = _check_sum_is_none(all_output_query['output_tree__sum'])

            result = {
                "all_plan": all_plan,
                "all_count": all_count,
                "all_amount": all_amount,
                "all_payout": all_payout,
                "all_output": all_output,
            }
            ctx = {"data": data, "form": form, "start": start, "end": end, "result": result}
        else:
            ctx = {"form": form, "start": start, "end": end}
        return render(request, self.template_name, ctx)


class TreeContractDepartmentReport(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/tree_contract/reports/department.html'

    def get(self, request, pk):
        current_year = date.today().year
        start = date(current_year, 1, 1).strftime('%Y-%m-%d')
        end_date = date(current_year, 12, 31).strftime('%Y-%m-%d')
        end = self.request.GET.get('end', None)
        if not end:
            end_dateformat = datetime.strptime(end_date, '%Y-%m-%d')
            current_month = end_dateformat.month
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.strptime(end, '%Y-%m-%d')
            current_month = end_dateformat.month
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = end_dateformat.strftime('%Y-%m-%d')

        form = FilterForm(initial={"start": start, "end": end})
        department = Department.objects.filter(id=pk)[0]
        if department:
            plan_data = TreeContractPlan.objects.filter(department=department,
                                                        date__year=current_year, status=1)
            actual_data = TreeContract.objects.filter(department=department,
                                                      date__range=[start, end_date], status=1)
            tree_contract_category_list = TreeContractCategory.objects.filter(status=1)
            region_id = None,
            region_obj = None
            data = []
            x = 1
            for item in tree_contract_category_list:
                count_query = actual_data.filter(category=item).aggregate(Sum('count'))
                amount_query = actual_data.filter(category=item).aggregate(Sum('amount'))
                payout_query = actual_data.filter(category=item).aggregate(Sum('payout'))
                output_tree_query = actual_data.filter(category=item).aggregate(Sum('output_tree'))

                count = _check_sum_is_none(count_query['count__sum'])
                amount = _check_sum_is_none(amount_query['amount__sum'])
                payout = _check_sum_is_none(payout_query['payout__sum'])
                output_tree = _check_sum_is_none(output_tree_query['output_tree__sum'])
                data.append({
                    "category": item.name,
                    "count": count,
                    "amount": amount,
                    "payout": payout,
                    "output_tree": output_tree
                })
            tree_count_query = plan_data.aggregate(Sum('tree_count'))
            count_query = actual_data.aggregate(Sum('count'))
            amount_query = actual_data.aggregate(Sum('amount'))
            payout_query = actual_data.aggregate(Sum('payout'))
            output_tree_query = actual_data.aggregate(Sum('output_tree'))
            count = _check_sum_is_none(count_query['count__sum'])
            amount = _check_sum_is_none(amount_query['amount__sum'])
            payout = _check_sum_is_none(payout_query['payout__sum'])
            output_tree = _check_sum_is_none(output_tree_query['output_tree__sum'])
            tree_count = _check_sum_is_none(tree_count_query['tree_count__sum'])
            result = {
                "depart_name": department,
                "tree_count": tree_count,
                "count": count,
                "amount": amount,
                "payout": payout,
                "output_tree": output_tree,

            }
            # for depart in departments:
            #     x = x + 1
            #     # PRODUCTION
            #     depart_plan_query = plan_data.filter(department=depart).aggregate(Sum('tree_count'))
            #     depart_count_query = actual_data.filter(department=depart).aggregate(Sum('count'))
            #     depart_amount_query = actual_data.filter(department=depart).aggregate(Sum('amount'))
            #     depart_payout_query = actual_data.filter(department=depart).aggregate(Sum('payout'))
            #     depart_output_query = actual_data.filter(department=depart).aggregate(Sum('output_tree'))
            #
            #     depart_count = _check_sum_is_none(depart_count_query['count__sum'])
            #     depart_amount = _check_sum_is_none(depart_amount_query['amount__sum'])
            #     depart_payout = _check_sum_is_none(depart_payout_query['payout__sum'])
            #     depart_output = _check_sum_is_none(depart_output_query['output_tree__sum'])
            #     depart_plan = _check_sum_is_none(depart_plan_query['tree_count__sum'])
            #
            #     # PAID SERVICE
            #     if region_id != depart.region_id:
            #         # PRODUCTION
            #         region_obj = Region.objects.get(id=depart.region_id)
            #         region_plan_query = plan_data.filter(region=region_obj).aggregate(Sum('tree_count'))
            #         region_count_query = actual_data.filter(region=region_obj).aggregate(Sum('count'))
            #         region_amount_query = actual_data.filter(region=region_obj).aggregate(Sum('amount'))
            #         region_payout_query = actual_data.filter(region=region_obj).aggregate(Sum('payout'))
            #         region_output_query = actual_data.filter(region=region_obj).aggregate(Sum('output_tree'))
            #
            #         region_count = _check_sum_is_none(region_count_query['count__sum'])
            #         region_amount = _check_sum_is_none(region_amount_query['amount__sum'])
            #         region_payout = _check_sum_is_none(region_payout_query['payout__sum'])
            #         region_output = _check_sum_is_none(region_output_query['output_tree__sum'])
            #         region_plan = _check_sum_is_none(region_plan_query['tree_count__sum'])
            #
            #         data.append({
            #             "index": 1,
            #             "region_id": region_obj.id,
            #             "region_plan": region_plan,
            #             "region_name": region_obj.name,
            #             "region_count": region_count,
            #             "region_amount": region_amount,
            #             "region_payout": region_payout,
            #             "region_output": region_output,
            #
            #             "depart_name": depart.name,
            #             "depart_id": depart.id,
            #             "depart_plan": depart_plan,
            #             "depart_count": depart_count,
            #             "depart_amount": depart_amount,
            #             "depart_payout": depart_payout,
            #             "depart_output": depart_output
            #         })
            #         x = 1
            #     else:
            #         data.append({
            #             "index": x,
            #             "depart_id": depart.id,
            #             "depart_name": depart.name,
            #             "depart_count": depart_count,
            #             "depart_amount": depart_amount,
            #             "depart_payout": depart_payout,
            #             "depart_output": depart_output,
            #             "depart_plan": depart_plan
            #         })
            #     region_obj = None
            #     region_id = depart.region_id
            # all_plan_query = TreeContractPlan.objects.filter(date__year=current_year, status=1).aggregate(
            #     Sum('tree_count'))
            # all_count_query = TreeContract.objects.filter(status=1, date__year=current_year).aggregate(Sum('count'))
            # all_amount_query = TreeContract.objects.filter(status=1, date__year=current_year).aggregate(Sum('amount'))
            # all_payout_query = TreeContract.objects.filter(status=1, date__year=current_year).aggregate(Sum('payout'))
            # all_output_query = TreeContract.objects.filter(status=1, date__year=current_year).aggregate(
            #     Sum('output_tree'))
            #
            # all_plan = _check_sum_is_none(all_plan_query['tree_count__sum'])
            # all_count = _check_sum_is_none(all_count_query['count__sum'])
            # all_amount = _check_sum_is_none(all_amount_query['amount__sum'])
            # all_payout = _check_sum_is_none(all_payout_query['payout__sum'])
            # all_output = _check_sum_is_none(all_output_query['output_tree__sum'])

            # result = {
            #     "all_plan": all_plan,
            #     "all_count": all_count,
            #     "all_amount": all_amount,
            #     "all_payout": all_payout,
            #     "all_output": all_output,
            # }
            ctx = {"data": data, "form": form, "start": start, "end": end, "result": result}
            return render(request, self.template_name, ctx)
        else:
            ctx = {"form": form, "start": start, "end": end}
            return render(request, self.template_name, ctx)


class TreeCategoryList(LoginRequiredMixin, ListView):
    template_name = 'urmon_barpo/trees/category/list.html'
    paginate_by = 10
    model = TreeHeightReport

    def get_context_data(self, *args, **kwargs):
        context = super(TreeCategoryList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return TreeCategory.objects.exclude(status=2).order_by('-id')


class TreeCategoryCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/trees/category/create.html'

    def get(self, request):
        try:
            form = TreeCategoryForm()
            context = {
                "is_user": True, "form": form,
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request):
        try:
            form = TreeCategoryForm(data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:category_list')
            else:
                return redirect('trees:category_list')
        except ObjectDoesNotExist:
            return redirect('trees:category_list')


class TreeCategoryDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/trees/category/detail.html'

    def get(self, request, pk):
        try:
            category = TreeCategory.objects.get(pk=pk)
            form = TreeCategoryForm(initial={"name": category.name})
            context = {
                "is_user": True,
                'form': form,
                "category": category
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            tree = TreeCategory.objects.get(pk=pk)
            form = TreeCategoryForm(instance=tree, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:category_list')
            else:
                return redirect('trees:category_list')
        except ObjectDoesNotExist:
            return redirect('trees:category_list')


class TreeCategoryDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/trees/category/list.html'

    def get(self, request, pk):
        qs = TreeCategory.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:category_list')
        else:
            return redirect('trees:category_list')


# Sapling Actual-> Ko'chat
class SaplingList(LoginRequiredMixin, FilterView, ListView):
    model = Sapling
    context_object_name = 'object_list'
    template_name = 'urmon_barpo/sapling/sapling_list.html'
    paginate_by = 10
    filterset_class = SaplingActualFilter

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
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return Sapling.objects.filter(region__in=regions, department__in=departments, status=1).order_by('-id')
        else:
            return Sapling.objects.filter(status=44)


class SaplingCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/sapling_create.html'

    def get(self, request):
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        tree_plant = serialize('json', TreePlant.objects.filter(status=1, is_show_sprouting=True).order_by('sort'))
        ctx = {"departments": departments, "regions": regions,
               "tree_plants": tree_plant, }
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        items = json.loads(data['items'])
        for i in range(len(items)):
            Sapling.objects.create(
                date=data['date'],
                department=Department.objects.get(id=data['department']),
                region=Region.objects.get(id=data['region']),
                count=items[i]['count'],
                plant=TreePlant.objects.get(id=items[i]['tree_plant']),
                creator=self.request.user
            )
        return redirect('trees:sapling_list')


class SaplingDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/sapling_detail.html'

    def get(self, request, pk):
        try:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            sapling = Sapling.objects.get(pk=pk)
            form = SaplingForm(initial={
                'date': sapling.date,
                "count": sapling.count,
                "department": sapling.department,
                "creator": sapling.creator,
                "region": sapling.region,
                "plant": sapling.plant})
            context = {
                "is_user": True,
                "sapling": sapling,
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
            sapling = Sapling.objects.get(pk=pk)
            form = SaplingForm(instance=sapling, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:sapling_list')
            else:
                return redirect('trees:sapling_list')
        except ObjectDoesNotExist:
            return redirect('trees:sapling_list')


class SaplingDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/sapling_list.html'
    permission_required = 'trees.delete_sapling'

    def get(self, request, pk):
        qs = Sapling.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:sapling_list')
        else:
            return redirect('trees:sapling_list')


# SaplingPlan -> Kochat
class SaplingDashboard(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/dashboard.html'

    def get(self, request):
        return render(request, self.template_name, )


# YOPIQ ILDIZLI DASHBOARD
class YopiqIldizDashboard(LoginRequiredMixin, View):
    template_name = "urmon_barpo/yopiq_ildiz_dashboard.html"

    def get(self, request):
        return render(request, self.template_name)


class SaplingPlanList(LoginRequiredMixin, ListView):
    template_name = 'urmon_barpo/sapling/sapling_plan/sapling_plan_list.html'
    paginate_by = 10
    model = SaplingPlan

    def get_context_data(self, *args, **kwargs):
        context = super(SaplingPlanList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return SaplingPlan.objects.filter(region__in=regions, department__in=departments, status=1).order_by('-id')
        else:
            return SaplingPlan.objects.filter(status=44)


class SaplingPlanCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/sapling_plan/sapling_plan_create.html'

    def get(self, request):
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        ctx = {"data": departments, "region": regions}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        next_state = json.loads(data['next'])
        today = date.today()
        today = today.strftime('%Y-%m-%d')
        SaplingPlan.objects.create(
            date=today,
            department=Department.objects.get(id=data['department']),
            region=Region.objects.get(id=data['region']),
            count=data['count'],
            creator=self.request.user
        )

        if next_state:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            ctx = {"data": departments, "region": regions}
            return render(request, self.template_name, ctx)
        else:
            return redirect('trees:sapling_plan_list')


class SaplingPlanDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/sapling_plan/sapling_plan_detail.html'

    def get(self, request, pk):
        try:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            sapling = SaplingPlan.objects.get(pk=pk)
            form = SaplingPlanForm(initial={
                'date': sapling.date,
                "count": sapling.count,
                "department": sapling.department,
                "creator": sapling.creator,
                "region": sapling.region,
                "plant": sapling.plant})
            context = {
                "is_user": True,
                "sapling": sapling,
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
            sapling = SaplingPlan.objects.get(pk=pk)
            form = SaplingPlanForm(instance=sapling, data=request.POST)
            if form.is_valid():
                res = form.cleaned_data['count']
                form.save()
                return redirect('trees:sapling_plan_list')
            else:
                return redirect('trees:sapling_plan_list')
        except ObjectDoesNotExist:
            return redirect('trees:sapling_plan_list')


class SaplingPlanDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/sapling_plan/sapling_plan_list.html'

    def get(self, request, pk):
        qs = SaplingPlan.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:sapling_plan_list')
        else:
            return redirect('trees:sapling_plan_list')


# SEED Actual --> URUG'
class SeedDashboard(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/seed/dashboard.html'

    def get(self, request):
        return render(request, self.template_name)


class SeedList(LoginRequiredMixin, FilterView, ListView):
    model = Seed
    context_object_name = 'object_list'
    template_name = 'urmon_barpo/seed/seed_list.html'
    paginate_by = 10
    filterset_class = SeedActualFilter

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
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return Seed.objects.filter(region__in=regions, department__in=departments, status=1).order_by('-id')
        else:
            return Seed.objects.filter(status=44).order_by('-id')


class SeedCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/seed/seed_create.html'
    permission_model = User

    def get(self, request):
        tree_plant = serialize('json', TreePlant.objects.filter(status=1, is_show_height=True))
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        ctx = {"data": departments, "region": regions,
               "tree_plant": tree_plant, }
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        items = json.loads(data['items'])
        for i in range(len(items)):
            Seed.objects.create(
                date=data['date'],
                department=Department.objects.get(id=data['department']),
                region=Region.objects.get(id=data['region']),
                count=int(items[i]['count']),
                plant=TreePlant.objects.get(id=items[i]['tree_plant']),
                creator=self.request.user
            )
        return redirect('trees:seed_list')


class SeedDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/seed/seed_detail.html'

    def get(self, request, pk):
        try:
            seed = Seed.objects.get(pk=pk)
            form = SeedForm(initial={
                'date': seed.date,
                "count": seed.count,
                "department": seed.department,
                "creator": seed.creator,
                "region": seed.region,
                "plant": seed.plant})
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "seed": seed,
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
            growing = Seed.objects.get(pk=pk)
            form = SeedForm(instance=growing, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:seed_list')
            else:
                return redirect('trees:seed_list')
        except ObjectDoesNotExist:
            return redirect('trees:seed_list')


class SeedDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/seed/seed_list.html'

    def get(self, request, pk):
        qs = Seed.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:seed_list')
        else:
            return redirect('trees:seed_list')


# SEED_PLAN
class SeedPlanList(LoginRequiredMixin, ListView):
    template_name = 'urmon_barpo/seed/seed_plan/seed_plan_list.html'
    paginate_by = 10
    model = SeedPlan

    def get_context_data(self, *args, **kwargs):
        context = super(SeedPlanList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return SeedPlan.objects.filter(region__in=regions, department__in=departments, status=1).order_by('-id')
        else:
            return SeedPlan.objects.filter(status=44).order_by('-id')


class SeedPlanCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/seed/seed_plan/seed_plan_create.html'

    def get(self, request):
        seed_list = serialize('json', TreePlant.objects.filter(status=1, is_show_height=True))
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        ctx = {"data": departments, "region": regions,
               "tree_plant": seed_list}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        nexxt = json.loads(data['next'])
        months = generate_month_year(int(data['date']))
        items = json.loads(data['items'])
        for i in range(len(items)):
            SeedPlan.objects.create(
                date=months[i],
                department=Department.objects.get(id=data['department']),
                region=Region.objects.get(id=data['region']),
                plant=TreePlant.objects.get(id=data['tree_plant']),
                count=int(items[i]['count']),
                creator=self.request.user
            )

        if nexxt:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            ctx = {"data": departments, "region": regions}
            return render(request, self.template_name, ctx)
        else:
            return redirect('trees:seed_plan_list')


class SeedPlanDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/seed/seed_plan/seed_plan_detail.html'

    def get(self, request, pk):
        try:
            seed = SeedPlan.objects.get(pk=pk)
            form = SeedPlanForm(initial={
                'date': seed.date,
                "count": seed.count,
                "department": seed.department,
                "creator": seed.creator,
                "region": seed.region,
                "plant": seed.plant})
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "seed": seed,
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
            seed = SeedPlan.objects.get(pk=pk)
            form = SeedPlanForm(instance=seed, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:seed_plan_list')
            else:
                return redirect('trees:seed_plan_list')
        except ObjectDoesNotExist:
            return redirect('trees:seed_plan_list')


class SeedPlanDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/seed/seed_plan/seed_plan_list.html'

    def get(self, request, pk):
        qs = SeedPlan.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:seed_plan_list')
        else:
            return redirect('trees:seed_plan_list')


# Spouting
class SproutDashboard(View):
    template_name = 'urmon_barpo/sprout/dashboard.html'
    permission_model = User

    def get(self, request):
        context = {"msg": "sa"}
        return render(request, self.template_name, context)


class SproutList(FilterView, ListView, LoginRequiredMixin):
    model = Sprout
    context_object_name = 'object_list'
    template_name = 'urmon_barpo/sprout/list.html'
    paginate_by = 10
    filterset_class = SproutActualFilter

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
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return Sprout.objects.filter(region__in=regions, department__in=departments, status=1).order_by('-id')
        else:
            return Sprout.objects.filter(status=44)


class SproutCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sprout/create.html'

    def get(self, request):
        regions = None
        departments = None
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        sprout_plant = serialize('json', TreePlant.objects.filter(status=1, is_show_sprouting=True))
        ctx = {"data": departments, "region": regions,
               "tree_plant": sprout_plant, }
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        items = json.loads(data['items'])
        for i in range(len(items)):
            Sprout.objects.create(
                date=data['date'],
                department=Department.objects.get(id=data['department']),
                region=Region.objects.get(id=data['region']),
                count=int(items[i]['count']),
                plant=TreePlant.objects.get(id=items[i]['tree_plant']),
                creator=self.request.user
            )
        return redirect('trees:sprout_list')


class SproutDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sprout/detail.html'
    permission_model = User

    def get(self, request, pk):
        try:
            sprout = Sprout.objects.get(pk=pk)
            form = SproutForm(initial={
                'date': sprout.date,
                "count": sprout.count,
                "department": sprout.department,
                "creator": sprout.creator,
                "region": sprout.region,
                "plant": sprout.plant})
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "sprout": sprout,
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
            sprout = Sprout.objects.get(pk=pk)
            form = SproutForm(instance=sprout, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:sprout_list')
            else:
                return redirect('trees:sprout_list')
        except ObjectDoesNotExist:
            return redirect('trees:sprout_list')


class SproutDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sprout/list.html'

    def get(self, request, pk):
        qs = Sprout.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:sprout_list')
        else:
            return redirect('trees:sprout_list')


class SproutPlanList(LoginRequiredMixin, ListView):
    template_name = 'urmon_barpo/sprout/sprout_plan/list.html'
    paginate_by = 10
    model = SproutPlan

    def get_context_data(self, *args, **kwargs):
        context = super(SproutPlanList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return SproutPlan.objects.filter(region__in=regions, department__in=departments, status=1).order_by('-id')
        else:
            return SproutPlan.objects.filter(status=44).order_by('-id')


class SproutPlanCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sprout/sprout_plan/create.html'

    def get(self, request):
        sprout_list = serialize('json', TreePlant.objects.filter(status=1, is_show_sprouting=True))
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        ctx = {"data": departments, "region": regions,
               "tree_plant": sprout_list}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        nexxt = json.loads(data['next'])
        months = generate_month_year(int(data['date']))
        items = json.loads(data['items'])
        for i in range(len(items)):
            SproutPlan.objects.create(
                date=months[i],
                department=Department.objects.get(id=data['department']),
                region=Region.objects.get(id=data['region']),
                plant=TreePlant.objects.get(id=data['tree_plant']),
                count=int(items[i]['count']),
                creator=self.request.user
            )

        if nexxt:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            ctx = {"data": departments, "region": regions}
            return render(request, self.template_name, ctx)
        else:
            return redirect('trees:sprout_plan_list')


class SproutPlanDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sprout/sprout_plan/detail.html'

    def get(self, request, pk):
        try:
            sprout = SproutPlan.objects.get(pk=pk)
            form = SproutPlanForm(initial={
                'date': sprout.date,
                "count": sprout.count,
                "department": sprout.department,
                "creator": sprout.creator,
                "region": sprout.region,
                "plant": sprout.plant})
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "sprout": sprout,
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
            sprout = SproutPlan.objects.get(pk=pk)
            form = SproutPlanForm(instance=sprout, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:sprout_plan_list')
            else:
                return redirect('trees:sprout_plan_list')
        except ObjectDoesNotExist:
            return redirect('trees:sprout_plan_list')


class SproutPlanDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sprout/sprout_plan/list.html'

    def get(self, request, pk):
        qs = SproutPlan.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:sprout_plan_list')
        else:
            return redirect('trees:sprout_plan_list')


# Sprout INPUT CRUD -> NIHOL KIRIM CRUD
class SproutInputList(LoginRequiredMixin, ListView):
    template_name = 'urmon_barpo/sprout/input/list.html'
    paginate_by = 10
    model = SproutInput

    def get_context_data(self, *args, **kwargs):
        context = super(SproutInputList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return SproutInput.objects.filter(region__in=regions, department__in=departments, status=1).order_by('-id')
        else:
            return SproutInput.objects.filter(status=44).order_by('-id')


class SproutInputCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sprout/input/create.html'
    permission_model = User

    def get(self, request):
        sprout_plant = serialize('json', TreePlant.objects.filter(status=1, is_show_sprouting=True))
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        ctx = {"data": departments,
               "region": regions,
               "tree_plant": sprout_plant}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        items = json.loads(data['items'])
        for i in range(len(items)):
            tree_category = TreePlant.objects.get(id=items[i]['tree_plant'])
            SproutInput.objects.create(
                date=data['date'],
                plant=TreePlant.objects.get(id=items[i]['tree_plant']),
                category=tree_category.category,
                donation=items[i]['donation'],
                buying=items[i]['buying'],
                new_sprout=items[i]['new_sprout'],
                department=Department.objects.get(id=data['department']),
                region=Region.objects.get(id=data['region']),
                creator=self.request.user
            )

        return redirect('trees:sprout_input_list')


class SproutInputDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sprout/input/detail.html'

    def get(self, request, pk):
        try:
            sprout = SproutInput.objects.get(id=pk)
            tree = TreePlant.objects.get(name=sprout.plant)
            form = SproutInputForm(initial={
                'date': sprout.date,
                "donation": sprout.donation,
                "buying": sprout.buying,
                "new_sprout": sprout.new_sprout,
                "department": sprout.department,
                "creator": sprout.creator,
                "region": sprout.region,
                "categories": tree.category,
                "plant": sprout.plant})
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "sprout": sprout,
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
            sprout = SproutInput.objects.get(pk=pk)
            form = SproutInputForm(instance=sprout, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:sprout_input_list')
            else:
                return redirect('trees:sprout_input_list')
        except ObjectDoesNotExist:
            return redirect('trees:sprout_input_list')


class SproutInputDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sprout/input/list.html'
    permission_model = User

    def get(self, request, pk):
        qs = SproutInput.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:sprout_input_list')
        else:
            return redirect('trees:sprout_input_list')


# Sprout OUTPUT CRUD -> NIHOL CHIQIM CRUD
class SproutOutputList(LoginRequiredMixin, ListView):
    template_name = 'urmon_barpo/sprout/output/list.html'
    paginate_by = 10
    model = SproutOutput

    def get_context_data(self, *args, **kwargs):
        context = super(SproutOutputList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return SproutOutput.objects.filter(region__in=regions, department__in=departments, status=1).order_by('-id')
        else:
            return SproutOutput.objects.filter(status=44).order_by('-id')


class SproutOutputCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sprout/output/create.html'

    def get(self, request):
        sprout_plants = serialize('json', TreePlant.objects.filter(status=1, is_show_sprouting=True))
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        ctx = {"data": departments,
               "region": regions,
               "tree_plant": sprout_plants}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        items = json.loads(data['items'])
        for i in range(len(items)):
            tree_category = TreePlant.objects.get(id=items[i]['tree_plant'])
            SproutOutput.objects.create(
                date=data['date'],
                plant=TreePlant.objects.get(id=items[i]['tree_plant']),
                category=tree_category.category,
                donation=items[i]['donation'],
                for_the_forest=items[i]['for_the_forest'],
                selling=items[i]['selling'],
                unsuccessful=items[i]['unsuccessful'],
                place_changed=items[i]['place_changed'],
                out_of_count=items[i]['out_of_count'],
                department=Department.objects.get(id=data['department']),
                region=Region.objects.get(id=data['region']),
                creator=self.request.user
            )
        return redirect('trees:sprout_output_list')


class SproutOutputDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sprout/output/detail.html'

    def get(self, request, pk):
        try:
            sprout = SproutOutput.objects.get(id=pk)
            tree = TreePlant.objects.get(name=sprout.plant)
            form = SproutOutputForm(initial={
                'date': sprout.date,
                "donation": sprout.donation,
                "selling": sprout.selling,
                "for_the_forest": sprout.for_the_forest,
                "unsuccessful": sprout.unsuccessful,
                "place_changed": sprout.place_changed,
                "out_of_count": sprout.out_of_count,
                "department": sprout.department,
                "creator": sprout.creator,
                "region": sprout.region,
                "categories": tree.category,
                "plant": sprout.plant})
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "sprout": sprout,
                "data": departments,
                "region": regions,
                'form': form
            }
            return render(request, self.template_name, context)
        except Exception as e:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            sprout = SproutOutput.objects.get(pk=pk)
            form = SproutOutputForm(instance=sprout, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:sprout_output_list')
            else:
                return redirect('trees:sprout_output_list')
        except ObjectDoesNotExist:
            return redirect('trees:sprout_output_list')


class SproutOutputDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sprout/output/list.html'

    def get(self, request, pk):
        qs = SproutOutput.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:sprout_output_list')
        else:
            return redirect('trees:sprout_output_list')


class SaplingInputList(LoginRequiredMixin, ListView):
    template_name = 'urmon_barpo/sapling/input/list.html'
    permission_required = 'trees.view_saplinginput'
    paginate_by = 10
    model = SaplingInput

    def get_context_data(self, *args, **kwargs):
        context = super(SaplingInputList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return SaplingInput.objects.filter(region__in=regions, department__in=departments, status=1).order_by('-id')
        else:
            return SaplingInput.objects.filter(status=44)


class SaplingInputCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/input/create.html'
    permission_required = 'trees.add_saplinginput'

    def get(self, request):
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        sapling_plant = serialize('json', TreePlant.objects.filter(status=1, is_show_height=True))
        ctx = {"data": departments,
               "region": regions,
               "tree_plant": sapling_plant}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        items = json.loads(data['items'])
        result = []
        for i in range(len(items)):
            tree_category = TreePlant.objects.get(id=items[i]['tree_plant'])
            result.append(SaplingInput.objects.create(
                date=data['date'],
                plant=TreePlant.objects.get(id=items[i]['tree_plant']),
                category=tree_category.category,
                donation=items[i]['donation'],
                buying=items[i]['buying'],
                new_sprout=items[i]['new_sprout'],
                department=Department.objects.get(id=data['department']),
                region=Region.objects.get(id=data['region']),
                creator=self.request.user
            ))
        return redirect('trees:sapling_input_list')


class SaplingInputDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/input/detail.html'
    permission_required = 'trees.view_saplinginput'

    def get(self, request, pk):
        try:
            sapling = SaplingInput.objects.get(pk=pk)
            tree = TreePlant.objects.get(name=sapling.plant)
            form = SaplingInputForm(initial={
                'date': sapling.date,
                "donation": sapling.donation,
                "buying": sapling.buying,
                "new_sprout": sapling.new_sprout,
                "department": sapling.department,
                "creator": sapling.creator,
                "region": sapling.region,
                "categories": tree.category,
                "plant": sapling.plant})
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "sapling": sapling,
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
            sapling = SaplingInput.objects.get(pk=pk)
            form = SaplingInputForm(instance=sapling, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:sapling_input_list')
            else:
                return redirect('trees:sapling_input_list')
        except ObjectDoesNotExist:
            return redirect('trees:sapling_input_list')


class SaplingInputDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/input/list.html'
    permission_required = 'trees.delete_saplinginput'

    def get(self, request, pk):
        qs = SaplingInput.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:sapling_input_list')
        else:
            return redirect('trees:sapling_input_list')


# SAPLING OUTPUT CRUD
class SaplingOutputList(LoginRequiredMixin, ListView):
    template_name = 'urmon_barpo/sapling/output/list.html'
    paginate_by = 10
    model = SaplingOutput

    def get_context_data(self, *args, **kwargs):
        context = super(SaplingOutputList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return SaplingOutput.objects.exclude(region__in=regions, department__in=departments, status=1).order_by(
                '-id')
        else:
            return SaplingOutput.objects.filter(status=44)


class SaplingOutputCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/output/create.html'

    def get(self, request):
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        sapling_plants = serialize('json', TreePlant.objects.filter(status=1, is_show_height=True))
        ctx = {"data": departments,
               "region": regions,
               "tree_plant": sapling_plants}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        items = json.loads(data['items'])
        for i in range(len(items)):
            tree_category = TreePlant.objects.get(id=items[i]['tree_plant'])
            SaplingOutput.objects.create(
                date=data['date'],
                plant=TreePlant.objects.get(id=items[i]['tree_plant']),
                category=tree_category.category,
                donation=items[i]['donation'],
                for_the_forest=items[i]['for_the_forest'],
                selling=items[i]['selling'],
                unsuccessful=items[i]['unsuccessful'],
                place_changed=items[i]['place_changed'],
                out_of_count=items[i]['out_of_count'],
                department=Department.objects.get(id=data['department']),
                region=Region.objects.get(id=data['region']),
                creator=self.request.user
            )
        return redirect('trees:sapling_output_list')


class SaplingOutputDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/output/detail.html'

    def get(self, request, pk):
        try:
            sapling = SaplingOutput.objects.get(pk=pk)
            tree = TreePlant.objects.get(name=sapling.plant)
            form = SaplingOutputForm(initial={
                'date': sapling.date,
                "donation": sapling.donation,
                "selling": sapling.selling,
                "for_the_forest": sapling.for_the_forest,
                "unsuccessful": sapling.unsuccessful,
                "place_changed": sapling.place_changed,
                "out_of_count": sapling.out_of_count,
                "department": sapling.department,
                "creator": sapling.creator,
                "region": sapling.region,
                "categories": tree.category,
                "plant": sapling.plant})
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "sapling": sapling,
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
            sprout = SaplingOutput.objects.get(pk=pk)
            form = SaplingOutputForm(instance=sprout, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:sapling_output_list')
            else:
                return redirect('trees:sapling_output_list')
        except ObjectDoesNotExist:
            return redirect('trees:sapling_output_list')


class SaplingOutputDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/output/list.html'

    def get(self, request, pk):
        qs = SaplingOutput.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:sapling_output_list')
        else:
            return redirect('trees:sapling_output_list')


# PREPAIRLAND URUG SEPISH
class PrePairReportDashboard(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/seed/reports/dashboard.html'

    def get(self, request):
        return render(request, self.template_name)


class PrepairLandDashboard(LoginRequiredMixin, View):
    template_name = "urmon_barpo/seed/land_dashboard.html"

    def get(self, request):
        return render(request, self.template_name)


class PrepairLandList(LoginRequiredMixin, FilterView, ListView):
    model = PrepairLand
    context_object_name = 'object_list'
    template_name = 'urmon_barpo/seed/land/list.html'
    paginate_by = 10
    filterset_class = PrepairLandActualFilter

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
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return PrepairLand.objects.filter(region__in=regions, department__in=departments, status=1).order_by('-id')
        else:
            return PrepairLand.objects.filter(status=44).order_by('-id')


class PrepairLandCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/seed/land/create.html'

    def get(self, request):
        land_categories = serialize('json', LandCategory.objects.filter(status=1))
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        ctx = {"data": departments, "region": regions,
               "land_categories": land_categories, }
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        items = json.loads(data['items'])
        for i in range(len(items)):
            PrepairLand.objects.create(
                date=data['date'],
                department=Department.objects.get(id=data['department']),
                region=Region.objects.get(id=data['region']),
                hectare=float(items[i]['hectare']),
                categories=LandCategory.objects.get(id=items[i]['category']),
                creator=self.request.user
            )
        return redirect('trees:land_list')


class PrepairLandDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/seed/land/detail.html'

    def get(self, request, pk):
        try:
            land = PrepairLand.objects.get(pk=pk)
            land_categories = LandCategory.objects.exclude(status=2)
            form = LandForm(initial={
                'date': land.date,
                "hectare": land.hectare,
                "department": land.department,
                "creator": land.creator,
                "region": land.region,
                "categories": land.categories})
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "land": land,
                "data": departments,
                "region": regions,
                "land_categories": land_categories,
                'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            land = PrepairLand.objects.get(pk=pk)
            form = LandForm(instance=land, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:land_list')
            else:
                return redirect('trees:land_list')
        except ObjectDoesNotExist:
            return redirect('trees:land_list')


class PrepairLandDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/seed/land/list.html'

    def get(self, request, pk):
        qs = PrepairLand.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:land_list')
        else:
            return redirect('trees:land_list')


class LandPlanList(LoginRequiredMixin, ListView):
    template_name = 'urmon_barpo/seed/land_plan/list.html'
    paginate_by = 10
    model = PrepairLand

    def get_context_data(self, *args, **kwargs):
        context = super(LandPlanList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return PrepairLandPlan.objects.filter(region__in=regions, department__in=departments, status=1).order_by(
                '-id')
        else:
            return PrepairLandPlan.objects.filter(status=44).order_by('-id')


class LandPlanCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/seed/land_plan/create.html'

    def get(self, request):
        land_categories = serialize('json', LandCategory.objects.filter(status=1))
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        ctx = {"data": departments, "region": regions,
               "land_categories": land_categories}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        nexxt = json.loads(data['next'])
        months = generate_month_year(int(data['date']))
        items = json.loads(data['items'])
        for i in range(len(items)):
            PrepairLandPlan.objects.create(
                date=months[i],
                department=Department.objects.get(id=data['department']),
                region=Region.objects.get(id=data['region']),
                categories=LandCategory.objects.get(id=data['category']),
                hectare=int(items[i]['hectare']),
                creator=self.request.user
            )

        if nexxt:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            ctx = {"data": departments, "region": regions}
            return render(request, self.template_name, ctx)
        else:
            return redirect('trees:land_plan_list')


class LandPlanDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/seed/land_plan/detail.html'

    def get(self, request, pk):

        try:
            land = PrepairLandPlan.objects.get(pk=pk)
            land_categories = LandCategory.objects.exclude(status=2)
            form = LandForm(initial={
                'date': land.date,
                "hectare": land.hectare,
                "department": land.department,
                "creator": land.creator,
                "region": land.region,
                "categories": land.categories})
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "land": land,
                "data": departments,
                "region": regions,
                "land_categories": land_categories,
                'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            land = PrepairLandPlan.objects.get(pk=pk)
            form = LandForm(instance=land, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:land_plan_list')
            else:
                return redirect('trees:land_plan_list')
        except ObjectDoesNotExist:
            return redirect('trees:land_plan_list')


class LandPlanDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/seed/land_plan/list.html'
    permission_model = User

    def get(self, request, pk):
        qs = PrepairLandPlan.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:land_plan_list')
        else:
            return redirect('trees:land_plan_list')


# PrepairLand INPUT OUTPUT REPORT
class PrepairLandReportView(LoginRequiredMixin, View):
    """
        http://127.0.0.1:8000/trees/seed/report
        shu pageda barcha regionlar va departmentlar
        o'rmon barpo qilish uchun qoyilgan plan va bajarilganlar
        ishlar xisoboti
        chiqadi va pratsenti xam korinadi va xar
        bir region departmentga bossa boladi va uni
        toliq xisobotini ko'rsa bo'ladi
    """
    template_name = 'urmon_barpo/seed/reports/regions_and_departments.html'

    def get(self, request):
        current_year = date.today().year
        end_date = date(current_year, 12, 31)
        year_end = self.request.GET.get('end', None)
        if not year_end:
            end_dateformat = end_date
            current_year = end_dateformat.year
            year_start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            year_end = date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.strptime(year_end, '%Y-%m-%d')
            current_year = end_dateformat.year
            year_start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            year_end = end_dateformat.strftime('%Y-%m-%d')
        result = []
        region_obj = None
        region_id = None
        plan_total = 0
        completed_total = 0
        data = []
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            land_data = PrepairLand.objects.filter(date__range=[year_start, year_end], status=1)
            land_plan_data = PrepairLandPlan.objects.filter(date__range=[year_start, year_end], status=1)
            form = FilterForm(initial={"start": year_start, "end": year_end})
            x = 1
            for department in departments:
                x = x + 1
                department_first_quarter = land_data.filter(date__quarter=1, department=department).aggregate(
                    Sum('hectare'))
                department_second_quarter = land_data.filter(date__quarter=2, department=department).aggregate(
                    Sum('hectare'))
                department_three_quarter = land_data.filter(date__quarter=3, department=department).aggregate(
                    Sum('hectare'))
                department_four_quarter = land_data.filter(date__quarter=4, department=department).aggregate(
                    Sum('hectare'))
                department_amount = land_plan_data.filter(department=department).aggregate(Sum('hectare'))
                department_completed = land_data.filter(department=department).aggregate(Sum('hectare'))
                if region_id != department.region_id:
                    region_obj = Region.objects.get(id=department.region_id)
                    region_amount = land_plan_data.filter(region=region_obj).aggregate(Sum('hectare'))
                    region_completed = land_data.filter(region=region_obj).aggregate(Sum('hectare'))
                    region_first_quarter = land_data.filter(date__quarter=1, region=region_obj).aggregate(
                        Sum('hectare'))
                    region_second_quarter = land_data.filter(date__quarter=2, region=region_obj).aggregate(
                        Sum('hectare'))
                    region_three_quarter = land_data.filter(date__quarter=3, region=region_obj).aggregate(
                        Sum('hectare'))
                    region_four_quarter = land_data.filter(date__quarter=4, region=region_obj).aggregate(Sum('hectare'))
                    plan_total += _check_sum_is_none(region_amount['hectare__sum'])
                    completed_total += _check_sum_is_none(region_completed['hectare__sum'])
                    data.append({
                        "index": 1,
                        "region_name": region_obj.name,
                        "region_id": region_obj.id,
                        "region_first_q": _check_sum_is_none(region_first_quarter['hectare__sum']),
                        "region_second_q": _check_sum_is_none(region_second_quarter['hectare__sum']),
                        "region_three_q": _check_sum_is_none(region_three_quarter['hectare__sum']),
                        "region_four_q": _check_sum_is_none(region_four_quarter['hectare__sum']),
                        "region_amount": _check_sum_is_none(region_amount['hectare__sum']),
                        "region_completed": _check_sum_is_none(region_completed['hectare__sum']),
                        "region_percentage": _calculate_percentage(region_amount['hectare__sum'],
                                                                   region_completed['hectare__sum']),
                        "department_name": department.name,
                        "department_id": department.id,
                        "department_first_q": _check_sum_is_none(department_first_quarter['hectare__sum']),
                        "department_second_q": _check_sum_is_none(department_second_quarter['hectare__sum']),
                        "department_three_q": _check_sum_is_none(department_three_quarter['hectare__sum']),
                        "department_four_q": _check_sum_is_none(department_four_quarter['hectare__sum']),
                        "department_amount": _check_sum_is_none(department_amount['hectare__sum']),
                        "department_completed": _check_sum_is_none(department_completed['hectare__sum']),
                        "department_percentage": _calculate_percentage(department_amount['hectare__sum'],
                                                                       department_completed['hectare__sum']),
                    })
                    x = 1
                else:
                    data.append({
                        "index": x,
                        "department_name": department.name,
                        "department_id": department.id,
                        "department_first_q": _check_sum_is_none(department_first_quarter['hectare__sum']),
                        "department_second_q": _check_sum_is_none(department_second_quarter['hectare__sum']),
                        "department_three_q": _check_sum_is_none(department_three_quarter['hectare__sum']),
                        "department_four_q": _check_sum_is_none(department_four_quarter['hectare__sum']),
                        "department_amount": _check_sum_is_none(department_amount['hectare__sum']),
                        "department_completed": _check_sum_is_none(department_completed['hectare__sum']),
                        "department_percentage": _calculate_percentage(department_amount['hectare__sum'],
                                                                       department_completed['hectare__sum']),
                    })
                region_obj = None
                region_id = department.region_id
            first = land_data.filter(date__quarter=1).aggregate(Sum('hectare'))
            second = land_data.filter(date__quarter=2).aggregate(Sum('hectare'))
            three = land_data.filter(date__quarter=3).aggregate(Sum('hectare'))
            four = land_data.filter(date__quarter=4).aggregate(Sum('hectare'))
            total_percentage = _calculate_percentage(plan_total, completed_total)
            context = {"form": form,
                       "data": data,
                       "first": _check_sum_is_none(first['hectare__sum']),
                       "second": _check_sum_is_none(second['hectare__sum']),
                       "three": _check_sum_is_none(three['hectare__sum']),
                       "four": _check_sum_is_none(four['hectare__sum']),
                       "total_percentage": total_percentage,
                       "plan_total": plan_total,
                       "completed_total": completed_total,
                       "start": year_start,
                       "end": year_end
                       }
            return render(request, self.template_name, context)
        else:
            form = FilterForm(initial={"start": year_start, "end": year_end})
            context = {"form": form, "start": year_start, "end": year_end}
            return render(request, self.template_name, context)


class PrepairLandDepartmentView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/seed/reports/department_detail.html'

    def get(self, request, pk):
        start = self.request.GET.get('start', None)
        end = self.request.GET.get('end', None)
        epoch_year = date.today().year
        year_start = date(epoch_year, 1, 1)
        year_end = date(epoch_year, 12, 31)
        form = FilterForm(initial={"start": year_start, "end": year_end})
        department = Department.objects.get(id=pk)
        land_categories_data = LandCategory.objects.filter(status=1)
        land_data = PrepairLand.objects.filter(department=department, date__range=[year_start, year_end], status=1)
        land_plan_data = PrepairLandPlan.objects.filter(department=department, date__range=[year_start, year_end],
                                                        status=1)
        data = []
        for category in land_categories_data:
            plan_sum = land_plan_data.filter(categories=category).aggregate(Sum('hectare'))
            first_q = land_data.filter(date__quarter=1, categories=category).aggregate(Sum('hectare'))
            second_q = land_data.filter(date__quarter=2, categories=category).aggregate(Sum('hectare'))
            three_q = land_data.filter(date__quarter=3, categories=category, ).aggregate(Sum('hectare'))
            four_q = land_data.filter(date__quarter=4, categories=category).aggregate(Sum('hectare'))
            data.append({
                "category": category.name,
                "first_q": _check_sum_is_none(first_q['hectare__sum']),
                "second_q": _check_sum_is_none(second_q['hectare__sum']),
                "three_q": _check_sum_is_none(three_q['hectare__sum']),
                "four_q": _check_sum_is_none(four_q['hectare__sum']),
                "plan_sum": _check_sum_is_none(plan_sum['hectare__sum'])
            })
        department_first_q = land_data.filter(date__quarter=1).aggregate(Sum('hectare'))
        department_second_q = land_data.filter(date__quarter=1).aggregate(Sum('hectare'))
        department_three_q = land_data.filter(date__quarter=1).aggregate(Sum('hectare'))
        department_four_q = land_data.filter(date__quarter=1).aggregate(Sum('hectare'))

        department_all_plan_sum = land_plan_data.aggregate(Sum('hectare'))
        department_collection = {
            "department_name": department.name,
            "department_first_q": _check_sum_is_none(department_first_q['hectare__sum']),
            "department_second_q": _check_sum_is_none(department_second_q['hectare__sum']),
            "department_three_q": _check_sum_is_none(department_three_q['hectare__sum']),
            "department_four_q": _check_sum_is_none(department_four_q['hectare__sum']),
            "department_all_plan_sum": _check_sum_is_none(department_all_plan_sum['hectare__sum'])
        }
        context = {"form": form, "department": department_collection, "data": data, "current_year": epoch_year}
        return render(request, self.template_name, context)


# SAPLING INPUT OUTPUT REPORT
class SaplingReportDashboardView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/report/dashboard.html'

    def get(self, request):
        return render(request, self.template_name)


class SaplingReportView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/report/regions_and_departments.html'

    def get(self, request):
        cur_year = date.today().year
        start_year = date(cur_year, 1, 1).strftime('%Y-%m-%d')
        start = self.request.GET.get('start', None)
        end = self.request.GET.get('end', None)
        if not end:
            end_dateformat = datetime.strptime(start_year, '%Y-%m-%d')
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            today = date.today()
            end = date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.strptime(end, '%Y-%m-%d')
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = end_dateformat.strftime('%Y-%m-%d')
        result = []
        region_obj = None
        region_id = None
        plan_total = 0
        completed_total = 0
        data = []
        form = FilterForm(initial={"start": start, "end": end})
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            sapling_plan_data = SaplingPlan.objects.filter(date__range=[start, end], status=1)
            sapling_actual_data = Sapling.objects.filter(date__range=[start, end], status=1)
            x = 1
            for department in departments:
                x = x + 1
                department_amount = sapling_plan_data.filter(department=department).aggregate(Sum('count'))
                department_completed = sapling_actual_data.filter(department=department).aggregate(Sum('count'))
                if region_id != department.region_id:
                    region_obj = Region.objects.get(id=department.region_id)
                    region_amount = sapling_plan_data.filter(region=region_obj).aggregate(Sum('count'))
                    region_completed = sapling_actual_data.filter(region=region_obj).aggregate(Sum('count'))

                    plan_total += _check_sum_is_none(region_amount['count__sum'])
                    completed_total += _check_sum_is_none(region_completed['count__sum'])
                    data.append({
                        "index": 1,
                        "region_name": region_obj.name,
                        "region_id": region_obj.id,
                        "region_amount": _check_sum_is_none(region_amount['count__sum']),
                        "region_completed": _check_sum_is_none(region_completed['count__sum']),
                        "region_percentage": _calculate_percentage(region_amount['count__sum'],
                                                                   region_completed['count__sum']),
                        "department_name": department.name,
                        "department_id": department.id,
                        "department_amount": _check_sum_is_none(department_amount['count__sum']),
                        "department_completed": _check_sum_is_none(department_completed['count__sum']),
                        "department_percentage": _calculate_percentage(department_amount['count__sum'],
                                                                       department_completed['count__sum']),
                    })
                    x = 1
                else:
                    data.append({
                        "index": x,
                        "department_name": department.name,
                        "department_id": department.id,
                        "department_amount": _check_sum_is_none(department_amount['count__sum']),
                        "department_completed": _check_sum_is_none(department_completed['count__sum']),
                        "department_percentage": _calculate_percentage(department_amount['count__sum'],
                                                                       department_completed['count__sum']),
                    })
                region_obj = None
                region_id = department.region_id
            total_percentage = _calculate_percentage(plan_total, completed_total)
            context = {"form": form,
                       "data": data,
                       "total_percentage": total_percentage,
                       "plan_total": plan_total,
                       "completed_total": completed_total,
                       "start": start,
                       "end": end
                       }
            return render(request, self.template_name, context)
        else:
            context = {"form": form, "start": start, "end": end}
            return render(request, self.template_name, context)


class SaplingRegionReportView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/report/region_report.html'

    def get(self, request, pk):
        trees_data = TreePlant.objects.filter(is_show_sprouting=True, status=1).order_by('-id')
        region = Region.objects.get(id=pk)
        department_data = Department.objects.filter(region=region, status=1)
        sapling_plan_db = SaplingPlan.objects.filter(region=region, date__range=[year_start, year_end])
        sapling_db = Sapling.objects.filter(region=region, date__range=[year_start, year_end])
        context = get_region_trees_data_for_report(trees_data, region, department_data, sapling_plan_db, sapling_db,
                                                   year_start, year_end)
        context['current_year'] = epoch_year
        return render(request, self.template_name, context)


class SaplingDepartmentReportView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/report/department_report.html'

    def get(self, request, pk):
        tree_plants = TreePlant.objects.filter(is_show_sprouting=True, status=1).order_by('sort')
        current_department = Department.objects.get(id=pk)
        sapling_plan_db = SaplingPlan.objects.filter(department=current_department,
                                                     date__range=[year_start, year_end])
        sapling_db = Sapling.objects.filter(department=current_department, date__range=[year_start, year_end])
        context = get_department_trees_data_for_report(sapling_plan_db, sapling_db, tree_plants, current_department)
        context['current_year'] = epoch_year
        context['department_name'] = current_department.name
        return render(request, self.template_name, context)


class SaplingRegionAllReport(LoginRequiredMixin, View):
    """
        http://127.0.0.1:8000/trees/sapling/all/report
        Ko'chatchilik kirim chiqim xisoboti uchun
        va bu pagedan departmentlarga bosib to'liq xolatini
        ko'rish mumkin
    """
    template_name = 'urmon_barpo/sapling/report/input_output_regions_and_department_report.html'

    def get(self, request):
        current_year = date.today().year
        start = date(current_year, 1, 1).strftime('%Y-%m-%d')
        end_date = date(current_year, 12, 31).strftime('%Y-%m-%d')
        end = self.request.GET.get('end', None)
        if not end:
            end_dateformat = datetime.strptime(end_date, '%Y-%m-%d')
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.strptime(end, '%Y-%m-%d')
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = end_dateformat.strftime('%Y-%m-%d')

        form = FilterForm(initial={"start": start, "end": end})
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            region_id = None
            region_obj = None
            sapling_input_data = SaplingInput.objects.filter(status=1, date__range=[start, end])
            sapling_output_data = SaplingOutput.objects.filter(status=1, date__range=[start, end])
            all_input = 0
            all_output = 0
            all_remainder = 0
            data = []
            x = 1
            for department in departments:
                x = x + 1
                # INPUT
                donation_in_query = sapling_input_data.filter(department=department, status=1).aggregate(
                    Sum('donation'))
                buying_in_query = sapling_input_data.filter(department=department, status=1).aggregate(Sum('buying'))
                new_sprout_in_query = sapling_input_data.filter(department=department, status=1).aggregate(
                    Sum('new_sprout'))
                # Checking is None
                in_donation = _check_sum_is_none(donation_in_query['donation__sum'])
                in_buying = _check_sum_is_none(buying_in_query['buying__sum'])
                in_new_sprout = _check_sum_is_none(new_sprout_in_query['new_sprout__sum'])
                input_sum = (in_donation + in_buying + in_new_sprout)
                # OUTPUT
                donation_out_query = sapling_output_data.filter(department=department, status=1).aggregate(
                    Sum('donation'))
                for_the_forest_out_query = sapling_output_data.filter(department=department, status=1).aggregate(
                    Sum('for_the_forest'))
                selling_out_query = sapling_output_data.filter(department=department, status=1).aggregate(
                    Sum('selling'))
                unsuccessful_out_query = sapling_output_data.filter(department=department, status=1).aggregate(
                    Sum('unsuccessful'))
                place_changed_out_query = sapling_output_data.filter(department=department, status=1).aggregate(
                    Sum('place_changed'))
                out_of_count_query = sapling_output_data.filter(department=department, status=1).aggregate(
                    Sum('out_of_count'))
                # Checking is None
                out_for_the_forest = _check_sum_is_none(donation_out_query['donation__sum'])
                out_donation = _check_sum_is_none(for_the_forest_out_query['for_the_forest__sum'])
                out_selling = _check_sum_is_none(selling_out_query['selling__sum'])
                out_unsuccessful = _check_sum_is_none(unsuccessful_out_query['unsuccessful__sum'])
                out_place_changed = _check_sum_is_none(place_changed_out_query['place_changed__sum'])
                out_of_count = _check_sum_is_none(out_of_count_query['out_of_count__sum'])
                output_sum = (
                        out_for_the_forest + out_donation + out_selling + out_unsuccessful + out_place_changed + out_of_count)
                remainder = input_sum - output_sum
                if region_id != department.region_id:
                    region_obj = Region.objects.get(id=department.region_id)
                    # INPUT
                    region_donation_in_query = sapling_input_data.filter(region=region_obj, status=1).aggregate(
                        Sum('donation'))
                    region_buying_in_query = sapling_input_data.filter(region=region_obj, status=1).aggregate(
                        Sum('buying'))
                    region_new_sprout_in_query = sapling_input_data.filter(region=region_obj, status=1).aggregate(
                        Sum('new_sprout'))
                    # Checking is None
                    region_in_donation = _check_sum_is_none(region_donation_in_query['donation__sum'])
                    region_in_buying = _check_sum_is_none(region_buying_in_query['buying__sum'])
                    region_in_new_sprout = _check_sum_is_none(region_new_sprout_in_query['new_sprout__sum'])
                    region_input_sum = (region_in_donation + region_in_buying + region_in_new_sprout)
                    all_input += region_input_sum
                    # OUTPUT
                    region_donation_out_query = sapling_output_data.filter(region=region_obj, status=1).aggregate(
                        Sum('donation'))
                    region_for_the_forest_out_query = sapling_output_data.filter(region=region_obj, status=1).aggregate(
                        Sum('for_the_forest'))
                    region_selling_out_query = sapling_output_data.filter(region=region_obj, status=1).aggregate(
                        Sum('selling'))
                    region_unsuccessful_out_query = sapling_output_data.filter(region=region_obj, status=1).aggregate(
                        Sum('unsuccessful'))
                    region_place_changed_out_query = sapling_output_data.filter(region=region_obj, status=1).aggregate(
                        Sum('place_changed'))
                    region_out_of_count_query = sapling_output_data.filter(region=region_obj, status=1).aggregate(
                        Sum('out_of_count'))
                    # Checking is None
                    region_out_for_the_forest = _check_sum_is_none(region_donation_out_query['donation__sum'])
                    region_out_donation = _check_sum_is_none(region_for_the_forest_out_query['for_the_forest__sum'])
                    region_out_selling = _check_sum_is_none(region_selling_out_query['selling__sum'])
                    region_out_unsuccessful = _check_sum_is_none(region_unsuccessful_out_query['unsuccessful__sum'])
                    region_out_place_changed = _check_sum_is_none(region_place_changed_out_query['place_changed__sum'])
                    region_out_of_count = _check_sum_is_none(region_out_of_count_query['out_of_count__sum'])
                    region_output_sum = (region_out_for_the_forest + region_out_donation + region_out_selling +
                                         region_out_unsuccessful + region_out_place_changed + region_out_of_count)
                    region_remainder = region_input_sum - region_output_sum

                    all_output += region_output_sum
                    all_remainder += region_remainder
                    data.append({
                        "index": 1,
                        "region_id": region_obj.id,
                        "region_name": region_obj.name,
                        "region_input_sum": region_input_sum,
                        "region_output_sum": region_output_sum,
                        "region_remainder": region_remainder,
                        "department_id": department.id,
                        "department_name": department.name,
                        "input_sum": input_sum,
                        "output_sum": output_sum,
                        "remainder": remainder
                    })
                    x = 1
                else:
                    data.append({
                        "index": x,
                        "department_id": department.id,
                        "department_name": department.name,
                        "input_sum": input_sum,
                        "output_sum": output_sum,
                        "remainder": remainder
                    })
                region_id = department.region_id
            context = {"form": form, "data": data, "start": start, "end": end,
                       "all_input": all_input, "all_output": all_output, "all_remainder": all_remainder}
        else:
            context = {"form": form, "start": start, "end": end}
        return render(request, self.template_name, context)


class SaplingDepartmentReport(LoginRequiredMixin, View):
    """
    http://127.0.0.1:8000/trees/sapling/all/report
    niholchilik kirim chiqim report pagedan turib
    departmentga bosganda shu class shu department uchun
    bolgan barcha input output ko'chatlar reportini qaytaradi
    example http://127.0.0.1:8000/trees/sapling/department/in/out/report/13
    """
    template_name = 'urmon_barpo/sapling/report/input_output_report.html'

    def get(self, request, pk):
        current_year = date.today().year
        end_date = date(current_year, 12, 31)
        year_end = self.request.GET.get('end', None)
        if not year_end:
            end_dateformat = end_date
            current_year = end_dateformat.year
            year_start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            year_end = date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.strptime(year_end, '%Y-%m-%d')
            current_year = end_dateformat.year
            year_start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            year_end = end_dateformat.strftime('%Y-%m-%d')
        department = Department.objects.get(id=pk)

        remainder_sum = get_sprout_remainder_sum(department.id, year_start)
        sapling_output_data = SaplingOutput.objects.filter(status=1, department=department,
                                                           date__range=[year_start, year_end])
        sapling_input_data = SaplingInput.objects.filter(status=1, department=department,
                                                         date__range=[year_start, year_end])
        all_count = get_all_sprout_input_output_sum(sapling_input_data, sapling_output_data)
        tree_categories_sql = get_sapling_input_output_tree_category_data(pk, year_start, year_end)
        trees_sql = get_department_sapling_input_output_tree_report_data(pk, year_start, year_end)
        all_count['remainder_sum'] = remainder_sum
        category_id = 0
        data = []
        for index, result in enumerate(trees_sql):
            data.append(result)
            category_id = result[0]
            if index == len(trees_sql) - 1 or category_id != trees_sql[index + 1][0]:
                for category in tree_categories_sql:
                    if category[0] == category_id:
                        data.append(category)
                        break

        form = FilterForm(initial={"start": year_start, "end": year_end})
        context = {"form": form, "data": data, "result": all_count, "department": department, "start": year_start,
                   "end": year_end}
        return render(request, self.template_name, context)


def get_sapling_remainder_sum(department_id=None, start=None):
    idd = str(department_id)
    year_start = datetime.strftime(start, '%Y-%m-%d')
    with connection.cursor() as cursor:
        query = f"""
                select (sum(si.donation) + sum(si.buying) + sum(si.new_sprout)) -
                (coalesce(sum(so.for_the_forest), 0) + coalesce(sum(so.unsuccessful),0)+ coalesce(sum(so.place_changed), 0)+ coalesce(sum(so.selling),0) 
                + coalesce(sum(so.donation),0) + coalesce(sum(so.out_of_count),0))
                from tree_plant tp1 left join sapling_input si on si.plant_id = tp1.id and si.date < '{year_start}' and si.department_id = {idd}
                left join sapling_output so on so.plant_id = tp1.id and so.date < '{year_start}' and so.department_id = {idd}  
        """
        cursor.execute(query)
        row = cursor.fetchall()
        return row[0]


# SPROUT INPUT OUTPUT REPORT
class SproutReportDashboard(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sprout/report/dashboard.html'

    def get(self, request):
        return render(request, self.template_name)


class SproutReportView(LoginRequiredMixin, View):
    """
        http://127.0.0.1:8000/trees/sapling/report
        shu pageda barcha regionlar va departmentlar
        uchun qoyilgan plan va bajarilganlar xisoboti
        chiqadi va pratsenti xam korinadi va xar
        bir region departmentga bossa boladi va uni
        toliq xisobotini ko'rsa bo'ladi
    """
    template_name = 'urmon_barpo/sprout/report/regions_and_departments.html'

    def get(self, request):
        current_year = date.today().year
        end_date = date(current_year, 12, 31)
        year_end = self.request.GET.get('end', None)
        if not year_end:
            end_dateformat = end_date
            current_year = end_dateformat.year
            year_start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            year_end = date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.strptime(year_end, '%Y-%m-%d')
            current_year = end_dateformat.year
            year_start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            year_end = end_dateformat.strftime('%Y-%m-%d')
        result = []
        region_obj = None
        region_id = None
        plan_total = 0
        completed_total = 0
        data = []
        form = FilterForm(initial={"start": year_start, "end": year_end})
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            x = 1
            for department in departments:
                x = x + 1
                department_amount = SproutPlan.objects.filter(date__range=[year_start, year_end],
                                                              department=department,
                                                              status=1).aggregate(Sum('count'))
                department_completed = Sprout.objects.filter(date__range=[year_start, year_end],
                                                             department=department,
                                                             status=1).aggregate(Sum('count'))
                if region_id != department.region_id:
                    region_obj = Region.objects.get(id=department.region_id)
                    region_amount = SproutPlan.objects.filter(date__range=[year_start, year_end],
                                                              region=region_obj, status=1).aggregate(Sum('count'))
                    region_completed = Sprout.objects.filter(date__range=[year_start, year_end],
                                                             region=region_obj, status=1).aggregate(Sum('count'))

                    plan_total += _check_sum_is_none(region_amount['count__sum'])
                    completed_total += _check_sum_is_none(region_completed['count__sum'])
                    data.append({
                        "index": 1,
                        "region_name": region_obj.name,
                        "region_id": region_obj.id,
                        "region_amount": _check_sum_is_none(region_amount['count__sum']),
                        "region_completed": _check_sum_is_none(region_completed['count__sum']),
                        "region_percentage": _calculate_percentage(region_amount['count__sum'],
                                                                   region_completed['count__sum']),
                        "department_name": department.name,
                        "department_id": department.id,
                        "department_amount": _check_sum_is_none(department_amount['count__sum']),
                        "department_completed": _check_sum_is_none(department_completed['count__sum']),
                        "department_percentage": _calculate_percentage(department_amount['count__sum'],
                                                                       department_completed['count__sum']),
                    })
                    x = 1
                else:
                    data.append({
                        "index": x,
                        "department_name": department.name,
                        "department_id": department.id,
                        "department_amount": _check_sum_is_none(department_amount['count__sum']),
                        "department_completed": _check_sum_is_none(department_completed['count__sum']),
                        "department_percentage": _calculate_percentage(department_amount['count__sum'],
                                                                       department_completed['count__sum']),
                    })
                region_obj = None
                region_id = department.region_id
            total_percentage = _calculate_percentage(plan_total, completed_total)
            context = {"form": form,
                       "data": data,
                       "total_percentage": total_percentage,
                       "plan_total": plan_total,
                       "completed_total": completed_total,
                       "start": year_start,
                       "end": year_end
                       }
            return render(request, self.template_name, context)
        else:
            context = {"form": form, "start": year_start, "end": year_end}
            return render(request, self.template_name, context)


class SproutRegionReportView(LoginRequiredMixin, View):
    """
        http://127.0.0.1:8000/trees/sprout/region/4
        bu class ga region_id keladi va shu region id ga
        bog'liq bolgan departmentlarni olib chiqib va ularga
        plan qilingan va bajarib bolingam Niholchilikga
        taluqli xisobotlar uchun

    """
    template_name = 'urmon_barpo/sprout/report/region_report.html'

    def get(self, request, pk):
        epoch_year = date.today().year
        year_start = date(epoch_year, 1, 1)
        year_end = datetime.now()
        trees_data = TreePlant.objects.filter(is_show_sprouting=True, status=1).order_by('-id')
        region = Region.objects.get(id=pk)
        department_data = Department.objects.filter(region=region, status=1)
        sapling_plan_db = SproutPlan.objects.filter(region=region, date__range=[year_start, year_end])
        sapling_db = Sprout.objects.filter(region=region, date__range=[year_start, year_end])
        context = get_region_trees_data_for_report(trees_data, region, department_data, sapling_plan_db, sapling_db,
                                                   year_start, year_end)
        return render(request, self.template_name, context)


class SproutDepartmentReportView(LoginRequiredMixin, View):
    """
        http://127.0.0.1:8000/trees/sprout/department/20
         bu class ga department_id keladi va shu department id ga
        bog'liq bolgan qo'yilgan  plan va bajarib bolingam Niholchilikga
        taluqli xisobotlar uchun
    """
    template_name = 'urmon_barpo/sprout/report/department_report.html'

    def get(self, request, pk):
        epoch_year = date.today().year
        year_start = date(epoch_year, 1, 1)
        year_end = datetime.now()
        tree_plants = TreePlant.objects.filter(is_show_height=True, status=1).order_by('-id')
        current_department = Department.objects.get(id=pk)
        sapling_plan_db = SproutPlan.objects.filter(department=current_department, date__range=[year_start, year_end])
        sapling_db = Sprout.objects.filter(department=current_department, date__range=[year_start, year_end])
        context = get_department_trees_data_for_report(sapling_plan_db, sapling_db, tree_plants, current_department)
        return render(request, self.template_name, context)


class SproutDepartmentReport(LoginRequiredMixin, View):
    """
    http://127.0.0.1:8000/trees/sprout/all/report
    niholchilik kirim chiqim report pagedan turib
    departmentga bosganda shu class shu department uchun
    bolgan barcha input output nihollar reportini qaytaradi
    example http://127.0.0.1:8000/trees/sprout/department/in/out/report/13
    """
    template_name = 'urmon_barpo/sprout/report/input_output_report.html'

    def get(self, request, pk):
        current_year = date.today().year
        end_date = date(current_year, 12, 31)
        year_end = self.request.GET.get('end', None)
        if not year_end:
            end_dateformat = end_date
            current_year = end_dateformat.year
            year_start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            year_end = date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.strptime(year_end, '%Y-%m-%d')
            current_year = end_dateformat.year
            year_start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            year_end = end_dateformat.strftime('%Y-%m-%d')
        department = Department.objects.get(id=pk)

        remainder_sum = get_sprout_remainder_sum(department.id, year_start)
        sprout_output_data = SproutOutput.objects.filter(status=1, department=department,
                                                         date__range=[year_start, year_end])
        sprout_input_data = SproutInput.objects.filter(status=1, department=department,
                                                       date__range=[year_start, year_end])
        all_count = get_all_sprout_input_output_sum(sprout_input_data, sprout_output_data)
        tree_categories_sql = get_input_output_tree_category_data(pk, year_start, year_end)
        trees_sql = get_department_input_output_tree_report_data(pk, year_start, year_end)
        all_count['remainder_sum'] = remainder_sum
        category_id = 0
        data = []
        for index, result in enumerate(trees_sql):
            data.append(result)
            category_id = result[0]
            if index == len(trees_sql) - 1 or category_id != trees_sql[index + 1][0]:
                for category in tree_categories_sql:
                    if category[0] == category_id:
                        data.append(category)
                        break

        form = FilterForm(initial={"start": year_start, "end": year_end})
        context = {"form": form, "data": data, "result": all_count, "department": department, "start": year_start,
                   "end": year_end}
        return render(request, self.template_name, context)


class SproutRegionAllReport(LoginRequiredMixin, View):
    """
        http://127.0.0.1:8000/trees/sprout/all/report
        Niholchilik kirim chiqim xisoboti uchun
        va bu pagedan departmentlarga bosib to'liq xolatini
        ko'rish mumkin
    """
    template_name = 'urmon_barpo/sprout/report/input_output_regions_and_department_report.html'

    def get(self, request):
        current_year = date.today().year
        end_date = date(current_year, 12, 31)
        year_end = self.request.GET.get('end', None)
        if not year_end:
            end_dateformat = end_date
            current_year = end_dateformat.year
            year_start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            year_end = date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.strptime(year_end, '%Y-%m-%d')
            current_year = end_dateformat.year
            year_start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            year_end = end_dateformat.strftime('%Y-%m-%d')
        form = FilterForm(initial={"start": year_start, "end": year_end})
        region_id = None
        region_obj = None
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            sprout_input_data = SproutInput.objects.filter(status=1, date__range=[year_start, year_end])
            sprout_output_data = SproutOutput.objects.filter(status=1, date__range=[year_start, year_end])
            all_input = 0
            all_output = 0
            all_remainder = 0
            data = []
            x = 1
            for department in departments:
                x = x + 1
                # INPUT
                donation_in_query = sprout_input_data.filter(department=department).aggregate(Sum('donation'))
                buying_in_query = sprout_input_data.filter(department=department).aggregate(Sum('buying'))
                new_sprout_in_query = sprout_input_data.filter(department=department).aggregate(Sum('new_sprout'))
                # Checking is None
                in_donation = _check_sum_is_none(donation_in_query['donation__sum'])
                in_buying = _check_sum_is_none(buying_in_query['buying__sum'])
                in_new_sprout = _check_sum_is_none(new_sprout_in_query['new_sprout__sum'])
                input_sum = (in_donation + in_buying + in_new_sprout)
                # OUTPUT
                donation_out_query = sprout_output_data.filter(department=department).aggregate(Sum('donation'))
                for_the_forest_out_query = sprout_output_data.filter(department=department).aggregate(
                    Sum('for_the_forest'))
                selling_out_query = sprout_output_data.filter(department=department).aggregate(Sum('selling'))
                unsuccessful_out_query = sprout_output_data.filter(department=department).aggregate(Sum('unsuccessful'))
                place_changed_out_query = sprout_output_data.filter(department=department).aggregate(
                    Sum('place_changed'))
                out_of_count_query = sprout_output_data.filter(department=department).aggregate(Sum('out_of_count'))
                # Checking is None
                out_for_the_forest = _check_sum_is_none(donation_out_query['donation__sum'])
                out_donation = _check_sum_is_none(for_the_forest_out_query['for_the_forest__sum'])
                out_selling = _check_sum_is_none(selling_out_query['selling__sum'])
                out_unsuccessful = _check_sum_is_none(unsuccessful_out_query['unsuccessful__sum'])
                out_place_changed = _check_sum_is_none(place_changed_out_query['place_changed__sum'])
                out_of_count = _check_sum_is_none(out_of_count_query['out_of_count__sum'])
                output_sum = input_sum - (
                        out_for_the_forest + out_donation + out_selling + out_unsuccessful + out_place_changed + out_of_count)
                remainder = (
                        out_for_the_forest + out_donation + out_selling + out_unsuccessful + out_place_changed + out_of_count)
                if region_id != department.region_id:
                    region_obj = Region.objects.get(id=department.region_id)
                    region_donation_in_query = sprout_input_data.filter(region=region_obj).aggregate(Sum('donation'))
                    region_buying_in_query = sprout_input_data.filter(region=region_obj).aggregate(Sum('buying'))
                    region_new_sprout_in_query = sprout_input_data.filter(region=region_obj).aggregate(
                        Sum('new_sprout'))
                    # Checking is None
                    region_in_donation = _check_sum_is_none(region_donation_in_query['donation__sum'])
                    region_in_buying = _check_sum_is_none(region_buying_in_query['buying__sum'])
                    region_in_new_sprout = _check_sum_is_none(region_new_sprout_in_query['new_sprout__sum'])
                    region_input_sum = (region_in_donation + region_in_buying + region_in_new_sprout)
                    all_input += region_input_sum
                    # OUTPUT
                    region_donation_out_query = sprout_output_data.filter(region=region_obj).aggregate(
                        Sum('donation'))
                    region_for_the_forest_out_query = sprout_output_data.filter(region=region_obj).aggregate(
                        Sum('for_the_forest'))
                    region_selling_out_query = sprout_output_data.filter(region=region_obj).aggregate(Sum('selling'))
                    region_unsuccessful_out_query = sprout_output_data.filter(region=region_obj).aggregate(
                        Sum('unsuccessful'))
                    region_place_changed_out_query = sprout_output_data.filter(region=region_obj).aggregate(
                        Sum('place_changed'))
                    region_out_of_count_query = sprout_output_data.filter(region=region_obj).aggregate(
                        Sum('out_of_count'))
                    # Checking is None
                    region_out_for_the_forest = _check_sum_is_none(region_donation_out_query['donation__sum'])
                    region_out_donation = _check_sum_is_none(region_for_the_forest_out_query['for_the_forest__sum'])
                    region_out_selling = _check_sum_is_none(region_selling_out_query['selling__sum'])
                    region_out_unsuccessful = _check_sum_is_none(region_unsuccessful_out_query['unsuccessful__sum'])
                    region_out_place_changed = _check_sum_is_none(region_place_changed_out_query['place_changed__sum'])
                    region_out_of_count = _check_sum_is_none(region_out_of_count_query['out_of_count__sum'])
                    region_output_sum = (region_out_for_the_forest + region_out_donation + region_out_selling +
                                         region_out_unsuccessful + region_out_place_changed + region_out_of_count)
                    region_remainder = region_input_sum - (
                            region_out_for_the_forest + region_out_donation + region_out_selling +
                            region_out_unsuccessful + region_out_place_changed + region_out_of_count)
                    all_output += region_output_sum
                    all_remainder += region_remainder
                    data.append({
                        "index": 1,
                        "region_id": region_obj.id,
                        "region_name": region_obj.name,
                        "region_input_sum": region_input_sum,
                        "region_output_sum": region_output_sum,
                        "region_remainder": region_remainder,
                        "department_id": department.id,
                        "department_name": department.name,
                        "input_sum": input_sum,
                        "output_sum": output_sum,
                        "remainder": remainder
                    })
                    x = 1
                else:
                    data.append({
                        "index": x,
                        "department_id": department.id,
                        "department_name": department.name,
                        "input_sum": input_sum,
                        "output_sum": output_sum,
                        "remainder": remainder
                    })
                region_id = department.region_id
            context = {"form": form, "data": data, "start": year_start, "end": year_end,
                       "all_input": all_input, "all_output": all_output, "all_remainder": all_remainder}
            return render(request, self.template_name, context)
        else:
            form = FilterForm(initial={"start": year_start, "end": year_end})
            context = {"form": form, "start": year_start, "end": year_end, }
            return render(request, self.template_name, context)


def get_sprout_remainder_sum(department_id=None, start=None):
    idd = str(department_id)
    with connection.cursor() as cursor:
        query = f"""
                        select (sum(si.donation) + sum(si.buying) + sum(si.new_sprout)) -
                        (coalesce(sum(so.for_the_forest), 0) + coalesce(sum(so.unsuccessful),0)+ coalesce(sum(so.place_changed), 0)+ coalesce(sum(so.selling),0) 
                        + coalesce(sum(so.donation),0) + coalesce(sum(so.out_of_count),0))
                        from tree_plant tp1 left join sprout_input si on si.plant_id = tp1.id and si.date < '{year_start}' and si.department_id = {idd}
                        left join sprout_output so on so.plant_id = tp1.id and so.date < '{year_start}' and so.department_id = {idd}  
                """
        cursor.execute(query)
        row = cursor.fetchall()
        return row[0]


class TreePlantReport(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/report/sapling_height_report.html'

    def get(self, request):
        current_year = date.today().year
        end_date = date(current_year, 12, 31)
        end = self.request.GET.get('end', None)
        if not end:
            end_dateformat = end_date
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.strptime(end, '%Y-%m-%d')
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = end_dateformat.strftime('%Y-%m-%d')
        form = FilterForm(initial={"start": start, "end": end})

        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            tree_names_data_in_db = TreePlant.objects.filter(status=1, is_show_height=True).order_by('sort')
            departments_data_in_db = departments.filter(status=1).order_by('sort')
            report = []
            region_id = None
            region_data = None,
            region_obj = None
            x = 1
            for depart_name in departments_data_in_db:
                x = x + 1
                department_trees = results(depart_name.id, start, end)
                department_tree_all_sum = get_department_tree_plant_sum(depart_name.id, start, end)
                if region_id != depart_name.region_id:
                    region_data = get_count_tree_plant(depart_name.region_id, start, end)
                    region_obj = Region.objects.get(id=depart_name.region_id)
                    region_tree_all_sum = get_region_tree_plant_sum(depart_name.region_id, start, end)
                    report.append({
                        "index": 1,
                        "department_name": depart_name.name,
                        "department_tree_all_sum": department_tree_all_sum,
                        "tree_height_report": department_trees,
                        "region_name": region_obj.name,
                        "all_count": region_data,
                        "region_tree_all_sum": region_tree_all_sum
                    })
                    x = 1
                else:
                    report.append({
                        "index": x,
                        "department_name": depart_name.name,
                        "department_tree_all_sum": department_tree_all_sum,
                        "tree_height_report": department_trees
                    })
                region_obj = None
                region_id = depart_name.region_id
            year_regions_and_deparment_tree_report = get_all_region_and_department_trees_sum(start, end)
            # DERARTMENLARDAGI DARAXTLAR YIGINDISI

            trees_sum = get_all_tress_sum(start, end)  # BARCHA DARAXTLAR SONI PLANDAGI
            context = {"form": form, "tree_names": tree_names_data_in_db,
                       "data": report,
                       "departments_all_tree_sum": year_regions_and_deparment_tree_report,
                       "trees_sum": trees_sum,
                       "start": start, "end": end}
        else:
            context = {"form": form, "start": start, "end": end}
        return render(request, self.template_name, context)


class TreeHeightReport2(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/sapling/report/tree_height_report.html'

    def get(self, request):
        current_year = date.today().year
        end_date = date(current_year, 12, 31)
        end = self.request.GET.get('end', None)
        if not end:
            end_dateformat = end_date
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.strptime(end, '%Y-%m-%d')
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = end_dateformat.strftime('%Y-%m-%d')
        form = FilterForm(initial={"start": start, "end": end})
        report = []
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            region_id = None
            region_obj = None
            all_first = 0
            all_second = 0
            all_tree = 0
            all_four = 0
            all_five = 0
            all_six = 0
            all_sum = 0
            x = 1
            for depart_name in departments:
                x = x + 1
                d_first = TreeHeightReport.objects.filter(
                    date__range=[start, end],
                    department=depart_name, status=1).aggregate(Sum('height_0_0_2_count'))
                d_second = TreeHeightReport.objects.filter(
                    date__range=[start, end],
                    department=depart_name, status=1).aggregate(Sum('height_0_2_5_count'))
                d_tree = TreeHeightReport.objects.filter(
                    date__range=[start, end],
                    department=depart_name, status=1).aggregate(Sum('height_0_5_1_count'))
                d_four = TreeHeightReport.objects.filter(
                    date__range=[start, end],
                    department=depart_name, status=1).aggregate(Sum('height_1_1_5_count'))
                d_five = TreeHeightReport.objects.filter(
                    date__range=[start, end],
                    department=depart_name, status=1).aggregate(Sum('height_1_5_2_count'))
                d_six = TreeHeightReport.objects.filter(
                    date__range=[start, end],
                    department=depart_name, status=1).aggregate(Sum('height_2_count'))
                d_first = _check_sum_is_none(d_first['height_0_0_2_count__sum'])
                d_second = _check_sum_is_none(d_second['height_0_2_5_count__sum'])
                d_tree = _check_sum_is_none(d_tree['height_0_5_1_count__sum'])
                d_four = _check_sum_is_none(d_four['height_1_1_5_count__sum'])
                d_five = _check_sum_is_none(d_five['height_1_5_2_count__sum'])
                d_six = _check_sum_is_none(d_six['height_2_count__sum'])
                d_sum = (d_first + d_second + d_tree + d_four + d_five + d_six)
                if region_id != depart_name.region_id:
                    region_obj = Region.objects.get(id=depart_name.region_id)
                    r_first = TreeHeightReport.objects.filter(
                        date__range=[start, end],
                        region=region_obj, status=1).aggregate(Sum('height_0_0_2_count'))
                    r_second = TreeHeightReport.objects.filter(
                        date__range=[start, end],
                        region=region_obj, status=1).aggregate(Sum('height_0_2_5_count'))
                    r_tree = TreeHeightReport.objects.filter(
                        date__range=[start, end],
                        region=region_obj, status=1).aggregate(Sum('height_0_5_1_count'))
                    r_four = TreeHeightReport.objects.filter(
                        date__range=[start, end],
                        region=region_obj, status=1).aggregate(Sum('height_1_1_5_count'))
                    r_five = TreeHeightReport.objects.filter(
                        date__range=[start, end],
                        region=region_obj, status=1).aggregate(Sum('height_1_5_2_count'))
                    r_six = TreeHeightReport.objects.filter(date__range=[start, end],
                                                            region=region_obj, status=1).aggregate(
                        Sum('height_2_count'))
                    r_first = _check_sum_is_none(r_first['height_0_0_2_count__sum'])
                    r_second = _check_sum_is_none(r_second['height_0_2_5_count__sum'])
                    r_tree = _check_sum_is_none(r_tree['height_0_5_1_count__sum'])
                    r_four = _check_sum_is_none(r_four['height_1_1_5_count__sum'])
                    r_five = _check_sum_is_none(r_five['height_1_5_2_count__sum'])
                    r_six = _check_sum_is_none(r_six['height_2_count__sum'])
                    r_sum = (r_first + r_second + r_tree + r_four + r_five + r_six)
                    all_first += r_first
                    all_second += r_second
                    all_tree += r_tree
                    all_four += r_four
                    all_five += r_five
                    all_six += r_six
                    all_sum += r_sum
                    report.append({
                        "index": 1,
                        "region_name": region_obj.name,
                        "region_first": r_first,
                        "region_second": r_second,
                        "region_tree": r_tree,
                        "region_four": r_four,
                        "region_five": r_five,
                        "region_six": r_six,
                        "region_sum": r_sum,

                        "department_id": depart_name.id,
                        "department_name": depart_name.name,
                        "department_sum": d_sum,
                        "department_first": d_first,
                        "department_second": d_second,
                        "department_tree": d_tree,
                        "department_four": d_four,
                        "department_five": d_five,
                        "department_six": d_six,
                    })
                    x = 1
                else:
                    report.append({
                        "index": x,
                        "department_id": depart_name.id,
                        "department_name": depart_name.name,
                        "department_sum": d_sum,
                        "department_first": d_first,
                        "department_second": d_second,
                        "department_tree": d_tree,
                        "department_four": d_four,
                        "department_five": d_five,
                        "department_six": d_six,
                    })
                region_obj = None
                region_id = depart_name.region_id
            all_result = {"all_first": all_first, "all_second": all_second, "all_tree": all_tree, "all_four": all_four,
                      "all_five": all_five, "all_six": all_six, "all_sum": all_sum}
            context = {'form': form, "data": report,
                   "all_result": all_result,
                   "start": start, "end": end}
        else:
            context = {'form': form, "data": report,
                       "start": start, "end": end}
        return render(request, self.template_name, context)


class TreeHeightDepartmentReport(View):
    template_name = 'urmon_barpo/sapling/report/tree_department_height_report.html'

    def get(self, request, pk):
        department = get_object_or_404(Department, id=pk)
        current_year = date.today().year
        end_date = date(current_year, 12, 31)
        end = self.request.GET.get('end', None)
        report = []
        if not end:
            end_dateformat = end_date
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.strptime(end, '%Y-%m-%d')
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = end_dateformat.strftime('%Y-%m-%d')
        tree_data = TreePlant.objects.filter(status=1, is_show_height=True).order_by('sort')
        for tree in tree_data:
            d_first = TreeHeightReport.objects.filter(date__range=[start, end],
                department=department, tree_plan=tree, status=1).aggregate(Sum('height_0_0_2_count'))
            d_second = TreeHeightReport.objects.filter(date__range=[start, end],
                department=department, tree_plan=tree, status=1).aggregate(Sum('height_0_2_5_count'))
            d_tree = TreeHeightReport.objects.filter(date__range=[start, end],
                department=department, tree_plan=tree, status=1).aggregate(Sum('height_0_5_1_count'))
            d_four = TreeHeightReport.objects.filter(date__range=[start, end],
                department=department, tree_plan=tree, status=1).aggregate(Sum('height_1_1_5_count'))
            d_five = TreeHeightReport.objects.filter(date__range=[start, end],
                department=department, tree_plan=tree, status=1).aggregate(Sum('height_1_5_2_count'))
            d_six = TreeHeightReport.objects.filter(date__range=[start, end],
                department=department, tree_plan=tree, status=1).aggregate(Sum('height_2_count'))
            d_first = _check_sum_is_none(d_first['height_0_0_2_count__sum'])
            d_second = _check_sum_is_none(d_second['height_0_2_5_count__sum'])
            d_tree = _check_sum_is_none(d_tree['height_0_5_1_count__sum'])
            d_four = _check_sum_is_none(d_four['height_1_1_5_count__sum'])
            d_five = _check_sum_is_none(d_five['height_1_5_2_count__sum'])
            d_six = _check_sum_is_none(d_six['height_2_count__sum'])
            d_sum = (d_first + d_second + d_tree + d_four + d_five + d_six)
            report.append({
                "tree_name": tree.name,
                "tree_first": d_first,
                "tree_second": d_second,
                "tree_tree": d_tree,
                "tree_four": d_four,
                "tree_five": d_five,
                "tree_six": d_six,
                "tree_sum": d_sum,
            })
        department_first = TreeHeightReport.objects.filter(date__range=[start, end],
            department=department, status=1).aggregate(Sum('height_0_0_2_count'))
        department_second = TreeHeightReport.objects.filter(date__range=[start, end],
            department=department, status=1).aggregate(Sum('height_0_2_5_count'))
        department_tree = TreeHeightReport.objects.filter(date__range=[start, end],
            department=department, status=1).aggregate(Sum('height_0_5_1_count'))
        department_four = TreeHeightReport.objects.filter(date__range=[start, end],
            department=department, status=1).aggregate(Sum('height_1_1_5_count'))
        department_five = TreeHeightReport.objects.filter(date__range=[start, end],
            department=department, status=1).aggregate(Sum('height_1_5_2_count'))
        department_six = TreeHeightReport.objects.filter(date__range=[start, end],
            department=department, status=1).aggregate(Sum('height_2_count'))
        department_first = _check_sum_is_none(department_first['height_0_0_2_count__sum'])
        department_second = _check_sum_is_none(department_second['height_0_2_5_count__sum'])
        department_tree = _check_sum_is_none(department_tree['height_0_5_1_count__sum'])
        department_four = _check_sum_is_none(department_four['height_1_1_5_count__sum'])
        department_five = _check_sum_is_none(department_five['height_1_5_2_count__sum'])
        department_six = _check_sum_is_none(department_six['height_2_count__sum'])
        department_sum = (department_first + department_second + department_tree +
                          department_four + department_five + department_six)
        all_sum = {"department_name": department.name,
                   "department_first": department_first,
                   "department_second": department_second,
                   "department_tree": department_tree,
                   "department_four": department_four,
                   "department_five": department_five,
                   "department_six": department_six,
                   "department_sum": department_sum}
        form = FilterForm(initial={"start": start, "end": end})
        context = {'form': form, "data": report,
                   "all_sum": all_sum, "start":start,
                   "end":end}
        return render(request, self.template_name, context)


def results(d_id=None, year_start=None, year_end=None):
    with connection.cursor() as cursor:
        idd = str(d_id)
        query = """select 
                    coalesce(thr.height_0_0_2_count,0) + 
                    coalesce(thr.height_0_2_5_count,0) + 
                    coalesce(thr.height_0_5_1_count,0) +
                    coalesce(thr.height_1_1_5_count,0) +
                    coalesce(thr.height_1_5_2_count,0) +
                    coalesce(thr.height_2_count,0)  summa,
                   thr.height_0_0_2_count, thr.height_0_2_5_count, thr.height_0_5_1_count,
                   thr.height_1_1_5_count, thr.height_1_5_2_count, thr.height_2_count from tree_height thr 
                   right join tree_plant tp on thr.tree_plan_id = tp.id and  thr.department_id = """ + idd + """ and thr.status=1 
                   and  thr.date BETWEEN '""" + year_start + """' AND '""" + year_end + """' where tp.is_show_height=TRUE order by tp.sort"""
        cursor.execute(query)
        row = cursor.fetchall()
        return row


def get_count_tree_plant(region_id=None, year_start='2021-01-01', year_end='2021-12-31'):
    with connection.cursor() as cursor:
        idd = str(region_id)
        query = f"""select  (
                    coalesce(sum(thr.height_0_0_2_count),0) + 
                    coalesce(sum(thr.height_0_2_5_count),0) + 
                    coalesce(sum(thr.height_0_5_1_count),0) +
                    coalesce(sum(thr.height_1_1_5_count),0) +
                    coalesce(sum(thr.height_1_5_2_count),0) +
                    coalesce(sum(thr.height_2_count),0) ) summa,
                   sum(thr.height_0_0_2_count) height_0_0_2_count_sum, sum(thr.height_0_2_5_count) height_0_0_2_count_sum, 
                   sum(thr.height_0_5_1_count) height_0_5_1_count_sum, sum(thr.height_1_1_5_count) height_1_1_5_count_sum, 
                   sum(thr.height_1_5_2_count) height_1_5_2_count_sum, sum(thr.height_2_count) height_2_count_sum
                   from tree_height thr
                   right join tree_plant tp  on thr.tree_plan_id = tp.id and thr.status=1 
                   and thr.region_id = {region_id} and  thr.date BETWEEN '{year_start}' AND '{year_end}'
                   where tp.is_show_height = True group by tp.id, thr.region_id order by tp.sort"""
        cursor.execute(query)
        row = cursor.fetchall()
        return row


def get_department_tree_plant_sum(department_id=None, year_start=None, year_end=None):
    """DEPARTMENTLARGA KIRITILGAN DARAXTLAR BARCHASINI YIGINDISI QAYTARADI """
    with connection.cursor() as cursor:
        query = f"""select (
                    coalesce(sum(thr.height_0_0_2_count),0) + 
                    coalesce(sum(thr.height_0_2_5_count),0) + 
                    coalesce(sum(thr.height_0_5_1_count),0) +
                    coalesce(sum(thr.height_1_1_5_count),0) +
                    coalesce(sum(thr.height_1_5_2_count),0) +
                    coalesce(sum(thr.height_2_count),0) ) summa
                    from tree_height thr
                    right join tree_plant tp on thr.tree_plan_id = tp.id and thr.date BETWEEN '{year_start}' AND '{year_end}'
                    and thr.status=1 
                    where thr.department_id = {department_id} and thr.status=1 and tp.is_show_height=TRUE group by thr.department_id """
        cursor.execute(query)
        row = cursor.fetchall()
        return row


def get_region_tree_plant_sum(region_id=None, year_start=None, year_end=None):
    with connection.cursor() as cursor:
        query = f"""select (
                    coalesce(sum(thr.height_0_0_2_count),0) + 
                    coalesce(sum(thr.height_0_2_5_count),0) + 
                    coalesce(sum(thr.height_0_5_1_count),0) +
                    coalesce(sum(thr.height_1_1_5_count),0) +
                    coalesce(sum(thr.height_1_5_2_count),0) +
                    coalesce(sum(thr.height_2_count),0) ) summa
                    from tree_height thr
                    right join tree_plant tp on thr.tree_plan_id = tp.id and thr.status=1
                    and thr.date BETWEEN '{year_start}' AND '{year_end}'
                    where thr.region_id = {region_id} AND tp.is_show_height = TRUE group by thr.region_id """
        cursor.execute(query)
        row = cursor.fetchall()
        return row


def get_all_region_and_department_trees_sum(start=None, end=None):
    with connection.cursor() as cursor:
        query = """select  sum(thr.height_0_0_2_count + thr.height_0_2_5_count + thr.height_0_5_1_count 
                    + thr.height_1_1_5_count + thr.height_1_5_2_count + thr.height_2_count) summa,
                    sum(thr.height_0_0_2_count), sum(thr.height_0_2_5_count), 
                    sum(thr.height_0_5_1_count), sum(thr.height_1_1_5_count), 
                    sum(thr.height_1_5_2_count), sum(thr.height_2_count) 
                    from tree_height thr
                    right join tree_plant tp  on thr.tree_plan_id = tp.id and thr.status=1 and  thr.date BETWEEN '""" + start + """' AND '""" + end + """'
                    where tp.is_show_height = TRUE  group by tp.id, tp.id order by tp.sort
        """

        cursor.execute(query)
        row = cursor.fetchall()
        return row


def get_all_tress_sum(start=None, end=None):
    with connection.cursor() as cursor:
        query = """select  sum(thr.height_0_0_2_count + thr.height_0_2_5_count + thr.height_0_5_1_count 
				    + thr.height_1_1_5_count + thr.height_1_5_2_count + thr.height_2_count) summa
                    from tree_height thr
                    right join tree_plant tp on thr.tree_plan_id = tp.id
                    where thr.date BETWEEN '""" + start + """' AND '""" + end + """' AND thr.status = 1 AND tp.is_show_height = TRUE
                    """
        cursor.execute(query)
        row = cursor.fetchall()
        return row[0]


def get_department_trees_data_for_report(plan_data=None, completed_data=None, trees=None, department=None):
    """Department ustiga bosganda shu departmentlarga qoshilgan daraxtlarni olib chiqib beradi"""
    trees_data = []
    for tree in trees:
        tp_plan_query = plan_data.filter(plant=tree).aggregate(Sum('count'))
        tp_comp_query = completed_data.filter(plant=tree,
                                              status=1).aggregate(Sum('count'))
        plan = _check_sum_is_none(tp_plan_query['count__sum'])
        completed = _check_sum_is_none(tp_comp_query['count__sum'])
        percentage = 0
        if plan and completed:
            percentage = _calculate_percentage(plan, completed)
        trees_data.append({
            "name": tree.name,
            "plan": plan,
            "completed": completed,
            "percentage": percentage
        })
    department_plan_sum_query = plan_data.filter(status=1).aggregate(Sum('count'))
    department_completed_sum_query = completed_data.filter(status=1).aggregate(Sum('count'))
    plan = _check_sum_is_none(department_plan_sum_query['count__sum'])
    completed = _check_sum_is_none(department_completed_sum_query['count__sum'])
    total_percentage = 0
    if plan and completed:
        total_percentage = _calculate_percentage(plan, completed)
    ctx = {"department_name": department.name,
           "department_plan": plan,
           "department_completed": completed,
           "department_percentage": total_percentage,
           "tree_plants": trees,
           "data": trees_data
           }
    return ctx


def get_region_trees_data_for_report(tree_plants=None, region=None, department_data=None, sapling_plan_db=None,
                                     sapling_db=None, year_start=None, year_end=None):
    data = []
    region_data = []
    index = 1
    for department in department_data:
        trees_data = []
        for tree in tree_plants:
            tp_plan_query = sapling_plan_db.filter(plant=tree, department=department,
                                                   status=1).aggregate(Sum('count'))
            tp_comp_query = sapling_db.filter(plant=tree, department=department,
                                              status=1).aggregate(Sum('count'))
            plan = _check_sum_is_none(tp_plan_query['count__sum'])
            completed = _check_sum_is_none(tp_comp_query['count__sum'])
            if index == 1:
                region_plan_query = sapling_plan_db.filter(plant=tree, region=region,
                                                           status=1).aggregate(Sum('count'))
                region_completed_query = sapling_db.filter(plant=tree,
                                                           region=region,
                                                           status=1).aggregate(Sum('count'))
                region_plan = _check_sum_is_none(region_plan_query['count__sum'])
                region_completed = _check_sum_is_none(region_completed_query['count__sum'])
                region_data.append({"plan": region_plan, "completed": region_completed})
            trees_data.append({
                "plan": plan,
                "completed": completed
            })
        index = index + 1
        department_plan_sum_query = sapling_plan_db.filter(department=department,
                                                           status=1).aggregate(Sum('count'))
        department_completed_sum_query = sapling_db.filter(department=department,
                                                           status=1).aggregate(Sum('count'))
        plan = _check_sum_is_none(department_plan_sum_query['count__sum'])
        completed = _check_sum_is_none(department_completed_sum_query['count__sum'])
        total_percentage = 0
        if plan and completed:
            total_percentage = _calculate_percentage(plan, completed)
        data.append({
            "department_name": department.name,
            "department_plan": plan,
            "department_completed": completed,
            "department_percentage": total_percentage,
            "child": trees_data
        })

    region_plan = SaplingPlan.objects.filter(date__range=[year_start, year_end],
                                             region=region, status=1).aggregate(Sum('count'))
    region_completed = Sapling.objects.filter(date__range=[year_start, year_end],
                                              region=region, status=1).aggregate(Sum('count'))
    region_plan_all_sum = _check_sum_is_none(region_plan['count__sum'])
    region_completed_all_sum = _check_sum_is_none(region_completed['count__sum'])
    total_percentage = _calculate_percentage(region_plan_all_sum, region_completed_all_sum)
    if region_plan_all_sum and region_completed_all_sum:
        total_percentage = _calculate_percentage(region_plan_all_sum, region_completed_all_sum)
    ctx = {"name": region.name,
           "all_plan": region_plan_all_sum,
           "all_completed": region_completed_all_sum,
           "all_percentage": total_percentage,
           "tree_plants": tree_plants,
           "region_data": region_data,
           "data": data
           }
    return ctx


def get_all_sprout_input_output_sum(sprout_input_data=None, sprout_output_data=None):
    """Niholchilik uchun barcha input outputlar yigindisini qaytaradi"""
    donation_in_query = sprout_input_data.aggregate(Sum('donation'))
    buying_in_query = sprout_input_data.aggregate(Sum('buying'))
    new_sprout_in_query = sprout_input_data.aggregate(Sum('new_sprout'))
    # Checking is None
    in_donation = _check_sum_is_none(donation_in_query['donation__sum'])
    in_buying = _check_sum_is_none(buying_in_query['buying__sum'])
    in_new_sprout = _check_sum_is_none(new_sprout_in_query['new_sprout__sum'])
    input_sum = (in_donation + in_buying + in_new_sprout)
    # OUTPUT
    donation_out_query = sprout_output_data.aggregate(Sum('donation'))
    for_the_forest_out_query = sprout_output_data.aggregate(Sum('for_the_forest'))
    selling_out_query = sprout_output_data.aggregate(Sum('selling'))
    unsuccessful_out_query = sprout_output_data.aggregate(Sum('unsuccessful'))
    place_changed_out_query = sprout_output_data.aggregate(Sum('place_changed'))
    out_of_count_out_query = sprout_output_data.aggregate(Sum('out_of_count'))
    # Checking is None
    out_for_the_forest = _check_sum_is_none(donation_out_query['donation__sum'])
    out_donation = _check_sum_is_none(for_the_forest_out_query['for_the_forest__sum'])
    out_selling = _check_sum_is_none(selling_out_query['selling__sum'])
    out_unsuccessful = _check_sum_is_none(unsuccessful_out_query['unsuccessful__sum'])
    out_place_changed = _check_sum_is_none(place_changed_out_query['place_changed__sum'])
    out_out_of_count = _check_sum_is_none(out_of_count_out_query['out_of_count__sum'])
    output_sum = input_sum - (
            out_for_the_forest + out_donation + out_selling + out_unsuccessful + out_place_changed + out_out_of_count)
    context = {
        "in_donation": in_donation,
        "in_buying": in_buying,
        "in_new_sprout": in_new_sprout,
        "input_sum": input_sum,
        "out_for_the_forest": out_for_the_forest,
        "out_donation": out_donation,
        "out_selling": out_selling,
        "out_unsuccessful": out_unsuccessful,
        "out_place_changed": out_place_changed,
        "out_out_of_count": out_out_of_count,
        "output_sum": output_sum
    }
    return context


def get_input_output_tree_category_data(department_id=None, start=None, end=None):
    """Niholchilik input output report department uchun daraxtlar categoriyasi"""
    with connection.cursor() as cursor:
        query = f"""
                 select tp.category_id, -1, tc.name, (select (coalesce(sum(si.donation),0) + coalesce(sum(si.buying),0) + coalesce(sum(si.new_sprout),0)) -
                (coalesce(sum(so.for_the_forest),0) + coalesce(sum(so.unsuccessful),0)+ coalesce(sum(so.place_changed),0)+ coalesce(sum(so.selling),0) 
									 + coalesce(sum(so.donation),0) + coalesce(sum(so.out_of_count), 0))
                 from tree_plant tp1 left join sprout_input si on si.plant_id = tp1.id and si.date < '{year_start}' and si.department_id = {department_id}
                 left join sprout_output so on so.plant_id = tp1.id and so.date < '{year_start}' and so.department_id = {department_id}
                 where tp1.category_id = tp.category_id) qoldiq,  coalesce(sum(si.donation),0), coalesce(sum(si.buying),0), coalesce(sum(si.new_sprout),0), 
                 (coalesce(sum(si.donation), 0) + coalesce(sum(si.buying),0) + coalesce(sum(si.new_sprout),0)),
                 coalesce(sum(so.for_the_forest),0),  coalesce(sum(so.unsuccessful),0), coalesce(sum(so.place_changed),0),  coalesce(sum(so.selling),0), 
                 coalesce(sum(so.donation),0), coalesce(sum(so.out_of_count),0), 
                 (coalesce(sum(si.donation),0) + coalesce(sum(si.buying),0) + coalesce(sum(si.new_sprout),0)) - 
                 (coalesce(sum(so.for_the_forest),0) + coalesce(sum(so.unsuccessful),0) + coalesce(sum(so.place_changed),0) + coalesce(sum(so.selling),0) 
				  + coalesce(sum(so.donation),0) + coalesce(sum(so.out_of_count),0) )
                 from tree_plant tp
                 left join tree_category tc on tc.id = tp.category_id
                 left join sprout_input si on si.plant_id = tp.id and si.date between '{year_start}' and '{year_end}' and si.department_id = {department_id}
                 left join sprout_output so on so.plant_id = tp.id and so.date between '{year_start}' and '{year_end}' and so.department_id = {department_id}
                 group by tp.category_id, tc.name order by tp.category_id
        """

        cursor.execute(query)
        row = cursor.fetchall()
        return row


def get_department_input_output_tree_report_data(department_id=None, start=None, end=None):
    """Niholchilik input output report department uchun daraxtlar data si """
    with connection.cursor() as cursor:
        query = f"""
                select tp.category_id,
                tp.id, tp.name, (select (coalesce(sum(si.donation),0) + coalesce(sum(si.buying),0) + coalesce(sum(si.new_sprout),0)) -
                (coalesce(sum(so.for_the_forest),0) + coalesce(sum(so.unsuccessful),0)+ coalesce(sum(so.place_changed),0)+ coalesce(sum(so.selling),0)
                 + coalesce(sum(so.donation),0) + coalesce(sum(so.out_of_count),0))
                from tree_plant tp1 left join sprout_input si on si.plant_id = tp1.id and si.date < '{year_start}' and si.department_id = {department_id}
                left join sprout_output so on so.plant_id = tp1.id and so.date < '{year_start}' and so.department_id = {department_id}
                where tp1.id = tp.id) qoldiq, sum(si.donation) donation, sum(si.buying) buying, sum(si.new_sprout) new_sprout, 
                (sum(si.donation) + sum(si.buying) +sum(si.new_sprout)) jami, 
                sum(so.for_the_forest),  sum(so.unsuccessful), sum(so.place_changed),  sum(so.selling),
                sum(so.donation), sum(so.out_of_count), 
                (coalesce(sum(si.donation),0) + coalesce(sum(si.buying),0) + coalesce(sum(si.new_sprout),0) ) - 
                (coalesce(sum(so.for_the_forest),0) + coalesce(sum(so.unsuccessful),0) + coalesce(sum(so.place_changed),0) + coalesce(sum(so.selling),0) 
                 + coalesce(sum(so.donation),0) + coalesce(sum(so.out_of_count),0))
                from tree_plant tp left join sprout_input si on si.plant_id = tp.id and si.date between '{year_start}' and '{year_end}' and si.department_id = {department_id}
                left join sprout_output so on so.plant_id = tp.id and so.date between '{year_start}' and '{year_end}' and so.department_id = {department_id} 
                group by tp.id, tp.name order by tp.category_id
        """
        cursor.execute(query)
        row = cursor.fetchall()
        return row


class TheGrowingPlantList(FilterView, ListView, LoginRequiredMixin):
    model = TreeGroundPlanting
    context_object_name = 'object_list'
    template_name = 'urmon_barpo/tree_ground_planting/list.html'
    paginate_by = 10
    filterset_class = TreeGroundPlantingActualFilter

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
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return TreeGroundPlanting.objects.filter(region__in=regions, department__in=departments, status=1).order_by(
                '-id')
        else:
            return TreeGroundPlanting.objects.filter(status=44).order_by('-id')


class TheGrowingPlantCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/tree_ground_planting/create.html'

    def get(self, request):
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        ctx = {"data": departments, "region": regions}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        items = json.loads(data['items'])
        if items:
            for i in range(len(items)):
                TreeGroundPlanting.objects.create(
                    date=data['date'],
                    department=Department.objects.get(id=data['department']),
                    region=Region.objects.get(id=data['region']),
                    desert_plant=items[i]['desert_plant'],
                    walnut=items[i]['walnut'],
                    pistachios=items[i]['pistachios'],
                    nut=items[i]['nut'],
                    poplar=items[i]['poplar'],
                    paulownia=items[i]['paulownia'],
                    other_plants=items[i]['other_plants'],
                    creator=self.request.user
                )
            return redirect('trees:the_growing_plant_list')
        else:
            return render(request, self.template_name, status=400)


class TheGrowingPlantDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/tree_ground_planting/detail.html'

    def get(self, request, pk):
        try:
            growing_plant = TreeGroundPlanting.objects.get(pk=pk)
            form = TheGroundPlantingForm(initial={
                'date': growing_plant.date,
                "desert_plant": growing_plant.desert_plant,
                "walnut": growing_plant.walnut,
                "pistachios": growing_plant.pistachios,
                "nut": growing_plant.nut,
                "poplar": growing_plant.poplar,
                "paulownia": growing_plant.paulownia,
                "other_plants": growing_plant.other_plants,
                "department": growing_plant.department,
                "creator": growing_plant.creator,
                "region": growing_plant.region,
            })
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "growing_plant": growing_plant,
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
            growing_plant = TreeGroundPlanting.objects.get(pk=pk)
            form = TheGroundPlantingForm(instance=growing_plant, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:the_growing_plant_list')
            else:
                return redirect('trees:the_growing_plant_list')
        except ObjectDoesNotExist:
            return redirect('trees:the_growing_plant_list')


class TheGrowingPlantDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/tree_ground_planting/list.html'

    def get(self, request, pk):
        qs = TreeGroundPlanting.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:the_growing_plant_list')
        else:
            return redirect('trees:the_growing_plant_list')


# TREE GROWING PLANTING PLAN
class TheGrowingPlantPlanList(LoginRequiredMixin, ListView):
    template_name = 'urmon_barpo/tree_ground_planting/plan/list.html'
    paginate_by = 10
    model = TreeGroundPlantingPlan

    def get_context_data(self, *args, **kwargs):
        context = super(TheGrowingPlantPlanList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return TreeGroundPlantingPlan.objects.filter(region__in=regions, department__in=departments,
                                                         status=1).order_by('-id')
        else:
            return TreeGroundPlantingPlan.objects.filter(status=44).order_by('-id')


class TheGrowingPlantPlanDeleteView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/tree_ground_planting/plan/list.html'

    def get(self, request, pk):
        qs = TreeGroundPlantingPlan.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('trees:the_growing_plant_plan_list')
        else:
            return redirect('trees:the_growing_plant_plan_list')


class TheGrowingPlantPlanCreate(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/tree_ground_planting/plan/create.html'

    def get(self, request):
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        sprout_list = serialize('json', TreePlant.objects.filter(status=1, is_show_sprouting=True))
        ctx = {"data": departments, "region": regions,
               "tree_plant": sprout_list}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        nexxt = json.loads(data['next'])
        TreeGroundPlantingPlan.objects.create(
            date=data['date'],
            department=Department.objects.get(id=data['department']),
            region=Region.objects.get(id=data['region']),
            desert_plant=data['desert_plant'],
            walnut=data['walnut'],
            pistachios=data['pistachios'],
            nut=data['nut'],
            poplar=data['poplar'],
            paulownia=data['paulownia'],
            other_plants=data['other_plants'],
            creator=self.request.user
        )
        if nexxt:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            ctx = {"data": departments, "region": regions}
            return render(request, self.template_name, ctx)
        else:
            return redirect('trees:the_growing_plant_plan_list')


class TheGrowingPlantPlanDetail(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/tree_ground_planting/plan/detail.html'

    def get(self, request, pk):
        try:
            growing_plant = TreeGroundPlantingPlan.objects.get(pk=pk)
            form = TheGroundPlantingPlanForm(initial={
                'date': growing_plant.date,
                "desert_plant": growing_plant.desert_plant,
                "walnut": growing_plant.walnut,
                "pistachios": growing_plant.pistachios,
                "nut": growing_plant.nut,
                "poplar": growing_plant.poplar,
                "paulownia": growing_plant.paulownia,
                "other_plants": growing_plant.other_plants,
                "department": growing_plant.department,
                "creator": growing_plant.creator,
                "region": growing_plant.region,
            })
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "growing_plant": growing_plant,
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
            growing_plant = TreeGroundPlantingPlan.objects.get(pk=pk)
            form = TheGroundPlantingPlanForm(instance=growing_plant, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('trees:the_growing_plant_plan_list')
            else:
                return redirect('trees:the_growing_plant_plan_list')
        except ObjectDoesNotExist:
            return redirect('trees:the_growing_plant_plan_list')


class TheGroundPlantingReportView(LoginRequiredMixin, View):
    template_name = 'urmon_barpo/tree_ground_planting/reports/regions_and_departments.html'

    def get(self, request):
        current_year = date.today().year
        end_date = date(current_year, 12, 31)
        year_end = self.request.GET.get('end', None)
        if not year_end:
            end_dateformat = end_date
            current_year = end_dateformat.year
            year_start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            year_end = date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.strptime(year_end, '%Y-%m-%d')
            current_year = end_dateformat.year
            year_start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            year_end = end_dateformat.strftime('%Y-%m-%d')
        result = []
        region_obj = None
        region_id = None
        plan_total = 0
        completed_total = 0
        data = []
        form = FilterForm(initial={"start": year_start, "end": year_end})
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            the_ground_planting_data = TreeGroundPlanting.objects.filter(date__year=current_year, status=1)
            the_ground_planting_plan_data = TreeGroundPlantingPlan.objects.filter(date__range=[year_start, year_end],
                                                                              status=1)
            x = 1
            for department in departments:
                x = x + 1
                # PLAN
                depart_plan_desert_plant_query = the_ground_planting_plan_data.filter(department=department).aggregate(
                    Sum('desert_plant'))
                depart_plan_walnut_query = the_ground_planting_plan_data.filter(department=department).aggregate(
                    Sum('walnut'))
                depart_plan_pistachios_query = the_ground_planting_plan_data.filter(department=department).aggregate(
                    Sum('pistachios'))
                depart_plan_nut_query = the_ground_planting_plan_data.filter(department=department).aggregate(
                    Sum('nut'))
                depart_plan_poplar_query = the_ground_planting_plan_data.filter(department=department).aggregate(
                    Sum('poplar'))
                depart_plan_paulownia_query = the_ground_planting_plan_data.filter(department=department).aggregate(
                    Sum('paulownia'))
                depart_plan_other_plants_query = the_ground_planting_plan_data.filter(department=department).aggregate(
                    Sum('other_plants'))

                depart_plan_desert = _check_sum_is_none(depart_plan_desert_plant_query['desert_plant__sum'])
                depart_plan_walnut = _check_sum_is_none(depart_plan_walnut_query['walnut__sum'])
                depart_plan_pistachios = _check_sum_is_none(depart_plan_pistachios_query['pistachios__sum'])
                depart_plan_nut = _check_sum_is_none(depart_plan_nut_query['nut__sum'])
                depart_plan_poplar = _check_sum_is_none(depart_plan_poplar_query['poplar__sum'])
                depart_plan_paulownia = _check_sum_is_none(depart_plan_paulownia_query['paulownia__sum'])
                depart_plan_other_plants = _check_sum_is_none(depart_plan_other_plants_query['other_plants__sum'])
                department_plan_all_sum = (depart_plan_desert + depart_plan_walnut + depart_plan_pistachios \
                                           + depart_plan_nut + depart_plan_poplar + depart_plan_paulownia \
                                           + depart_plan_other_plants)
                department_nut_plan_sum = (depart_plan_walnut + depart_plan_pistachios + depart_plan_nut)
                department_fast_growing_plan_sum = depart_plan_poplar + depart_plan_paulownia
                # amalda
                depart_comp_desert_plant_query = the_ground_planting_data.filter(department=department).aggregate(
                    Sum('desert_plant'))
                depart_comp_walnut_query = the_ground_planting_data.filter(department=department).aggregate(
                    Sum('walnut'))
                depart_comp_pistachios_query = the_ground_planting_data.filter(department=department).aggregate(
                    Sum('pistachios'))
                depart_comp_nut_query = the_ground_planting_data.filter(department=department).aggregate(Sum('nut'))
                depart_comp_poplar_query = the_ground_planting_data.filter(department=department).aggregate(
                    Sum('poplar'))
                depart_comp_paulownia_query = the_ground_planting_data.filter(department=department).aggregate(
                    Sum('paulownia'))
                depart_comp_other_plants_query = the_ground_planting_data.filter(department=department).aggregate(
                    Sum('other_plants'))

                depart_comp_desert = _check_sum_is_none(depart_comp_desert_plant_query['desert_plant__sum'])
                depart_comp_walnut = _check_sum_is_none(depart_comp_walnut_query['walnut__sum'])
                depart_comp_pistachios = _check_sum_is_none(depart_comp_pistachios_query['pistachios__sum'])
                depart_comp_nut = _check_sum_is_none(depart_comp_nut_query['nut__sum'])
                depart_comp_poplar = _check_sum_is_none(depart_comp_poplar_query['poplar__sum'])
                depart_comp_paulownia = _check_sum_is_none(depart_comp_paulownia_query['paulownia__sum'])
                depart_comp_other_plants = _check_sum_is_none(depart_comp_other_plants_query['other_plants__sum'])

                department_comp_all_sum = (depart_comp_desert + depart_comp_walnut + depart_comp_pistachios \
                                           + depart_comp_nut + depart_comp_poplar + depart_comp_paulownia \
                                           + depart_comp_other_plants)

                department_nut_comp_sum = depart_comp_walnut + depart_comp_pistachios + depart_comp_nut
                department_fast_growing_comp_sum = depart_comp_poplar + depart_comp_paulownia
                department_percentage = 0
                if department_plan_all_sum and department_comp_all_sum:
                    department_percentage = _calculate_percentage(department_plan_all_sum, department_comp_all_sum)
                if region_id != department.region_id:
                    region_obj = Region.objects.get(id=department.region_id)
                    # PLAN
                    region_plan_desert_plant_query = the_ground_planting_plan_data.filter(region=region_obj).aggregate(
                        Sum('desert_plant'))
                    region_plan_walnut_query = the_ground_planting_plan_data.filter(region=region_obj).aggregate(
                        Sum('walnut'))
                    region_plan_pistachios_query = the_ground_planting_plan_data.filter(region=region_obj).aggregate(
                        Sum('pistachios'))
                    region_plan_nut_query = the_ground_planting_plan_data.filter(region=region_obj).aggregate(
                        Sum('nut'))
                    region_plan_poplar_query = the_ground_planting_plan_data.filter(region=region_obj).aggregate(
                        Sum('poplar'))
                    region_plan_paulownia_query = the_ground_planting_plan_data.filter(region=region_obj).aggregate(
                        Sum('paulownia'))
                    region_plan_other_plants_query = the_ground_planting_plan_data.filter(region=region_obj).aggregate(
                        Sum('other_plants'))

                    region_plan_desert = _check_sum_is_none(region_plan_desert_plant_query['desert_plant__sum'])
                    region_plan_walnut = _check_sum_is_none(region_plan_walnut_query['walnut__sum'])
                    region_plan_pistachios = _check_sum_is_none(region_plan_pistachios_query['pistachios__sum'])
                    region_plan_nut = _check_sum_is_none(region_plan_nut_query['nut__sum'])
                    region_plan_poplar = _check_sum_is_none(region_plan_poplar_query['poplar__sum'])
                    region_plan_paulownia = _check_sum_is_none(region_plan_paulownia_query['paulownia__sum'])
                    region_plan_other_plants = _check_sum_is_none(region_plan_other_plants_query['other_plants__sum'])

                    region_plan_all_sum = (region_plan_desert + region_plan_walnut + region_plan_pistachios \
                                           + region_plan_nut + region_plan_poplar + region_plan_paulownia \
                                           + region_plan_other_plants)
                    region_nut_plan_sum = region_plan_walnut + region_plan_pistachios + region_plan_nut
                    region_fast_growing_plan_sum = region_plan_poplar + region_plan_paulownia
                    # AMALDA
                    region_comp_desert_plant_query = the_ground_planting_data.filter(region=region_obj).aggregate(
                        Sum('desert_plant'))
                    region_comp_walnut_query = the_ground_planting_data.filter(region=region_obj).aggregate(
                        Sum('walnut'))
                    region_comp_pistachios_query = the_ground_planting_data.filter(region=region_obj).aggregate(
                        Sum('pistachios'))
                    region_comp_nut_query = the_ground_planting_data.filter(region=region_obj).aggregate(Sum('nut'))
                    region_comp_poplar_query = the_ground_planting_data.filter(region=region_obj).aggregate(
                        Sum('poplar'))
                    region_comp_paulownia_query = the_ground_planting_data.filter(region=region_obj).aggregate(
                        Sum('paulownia'))
                    region_comp_other_plants_query = the_ground_planting_data.filter(region=region_obj).aggregate(
                        Sum('other_plants'))

                    region_comp_desert = _check_sum_is_none(region_comp_desert_plant_query['desert_plant__sum'])
                    region_comp_walnut = _check_sum_is_none(region_comp_walnut_query['walnut__sum'])
                    region_comp_pistachios = _check_sum_is_none(region_comp_pistachios_query['pistachios__sum'])
                    region_comp_nut = _check_sum_is_none(region_comp_nut_query['nut__sum'])
                    region_comp_poplar = _check_sum_is_none(region_comp_poplar_query['poplar__sum'])
                    region_comp_paulownia = _check_sum_is_none(region_comp_paulownia_query['paulownia__sum'])
                    region_comp_other_plants = _check_sum_is_none(region_comp_other_plants_query['other_plants__sum'])

                    region_comp_all_sum = (region_comp_desert + region_comp_walnut + region_comp_pistachios \
                                           + region_comp_nut + region_comp_poplar + region_comp_paulownia \
                                           + region_comp_other_plants)
                    region_percentage = 0
                    if region_plan_all_sum and region_comp_all_sum:
                        region_percentage = _calculate_percentage(region_plan_all_sum, region_comp_all_sum)
                    region_nut_comp_sum = region_comp_walnut + region_comp_pistachios + region_comp_nut
                    region_fast_growing_comp_sum = region_comp_poplar + region_comp_paulownia
                    data.append({
                        "index": 1,
                        "region_name": region_obj.name,
                        "region_plan": region_plan_all_sum,
                        "region_comp": region_comp_all_sum,
                        "region_percentage": region_percentage,
                        "region_desert_plant_plan": region_plan_desert,
                        "region_desert_plant_comp": region_comp_desert,
                        "region_nut_plan_sum": region_nut_plan_sum,
                        "region_nut_comp_sum": region_nut_comp_sum,
                        "region_plan_walnut": region_plan_walnut,
                        "region_comp_walnut": region_comp_walnut,
                        "region_plan_pistachios": region_plan_pistachios,
                        "region_comp_pistachios": region_comp_pistachios,
                        "region_plan_nut": region_plan_nut,
                        "region_comp_nut": region_comp_nut,
                        "region_fast_growing_plan_sum": region_fast_growing_plan_sum,
                        "region_fast_growing_comp_sum": region_fast_growing_comp_sum,
                        "region_plan_poplar": region_plan_poplar,
                        "region_comp_poplar": region_comp_poplar,
                        "region_plan_paulownia": region_plan_paulownia,
                        "region_comp_paulownia": region_comp_paulownia,
                        "region_plan_other_plants": region_plan_other_plants,
                        "region_comp_other_plants": region_comp_other_plants,

                        "department_name": department.name,
                        "department_plan": department_plan_all_sum,
                        "department_completed": department_comp_all_sum,
                        "department_percentage": department_percentage,
                        "department_desert_plant_plan": depart_plan_desert,
                        "department_desert_plant_comp": depart_comp_desert,
                        "department_nut_plan_sum": department_nut_plan_sum,
                        "department_nut_comp_sum": department_nut_comp_sum,
                        "depart_plan_walnut": depart_plan_walnut,
                        "depart_comp_walnut": depart_comp_walnut,
                        "depart_plan_pistachios": depart_plan_pistachios,
                        "depart_comp_pistachios": depart_comp_pistachios,
                        "depart_plan_nut": depart_plan_nut,
                        "depart_comp_nut": depart_comp_nut,
                        "department_fast_growing_plan_sum": department_fast_growing_plan_sum,
                        "department_fast_growing_comp_sum": department_fast_growing_comp_sum,
                        "department_plan_poplar": depart_plan_poplar,
                        "department_comp_poplar": depart_comp_poplar,
                        "department_plan_paulownia": depart_plan_paulownia,
                        "department_comp_paulownia": depart_comp_paulownia,
                        "department_plan_other_plants": depart_plan_other_plants,
                        "department_comp_other_plants": depart_comp_other_plants
                    })
                    x = 1
                else:
                    data.append({
                        "index": x,
                        "department_name": department.name,
                        "department_plan": department_plan_all_sum,
                        "department_completed": department_comp_all_sum,
                        "department_percentage": department_percentage,
                        "department_desert_plant_plan": depart_plan_desert,
                        "department_desert_plant_comp": depart_comp_desert,
                        "department_nut_plan_sum": department_nut_plan_sum,
                        "department_nut_comp_sum": department_nut_comp_sum,
                        "depart_plan_walnut": depart_plan_walnut,
                        "depart_comp_walnut": depart_comp_walnut,
                        "depart_plan_pistachios": depart_plan_pistachios,
                        "depart_comp_pistachios": depart_comp_pistachios,
                        "depart_plan_nut": depart_plan_nut,
                        "depart_comp_nut": depart_comp_nut,
                        "department_fast_growing_plan_sum": department_fast_growing_plan_sum,
                        "department_fast_growing_comp_sum": department_fast_growing_comp_sum,
                        "department_plan_poplar": depart_plan_poplar,
                        "department_comp_poplar": depart_comp_poplar,
                        "department_plan_paulownia": depart_plan_paulownia,
                        "department_comp_paulownia": depart_comp_paulownia,
                        "department_plan_other_plants": depart_plan_other_plants,
                        "department_comp_other_plants": depart_comp_other_plants
                    })
                region_obj = None
                region_id = department.region_id
            context = {"form": form,
                       "data": data,
                       "start": year_start,
                       "end": year_end,
                       "current_year": current_year}
            return render(request, self.template_name, context)
        else:
            context = {"form": form, "start": year_start, "end": year_end}
            return render(request, self.template_name, context)


"""Generate EXCEL reports ↓ ↓ ↓ .xlsx files"""


class TreeHeightReportXLSX(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/trees/sapling/height/report"""

    def get(self, request):
        from .excel.height_report import TreeHeightReportSheet
        start = request.GET.get('start')
        end = request.GET.get('end')
        if start and end:
            xlsx = TreeHeightReportSheet(user=self.request.user, start=start, end=end)
            return xlsx.generate_height_excel_report()
        else:
            messages.error(request, "Sana noto'g'ri kiritilgan")
            return render(request, 'urmon_barpo/sapling/report/sapling_height_report.html', {})


class SaplingPlanReportXLSX(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/trees/sapling/report"""

    def get(self, request):
        from .excel import sapling_report
        start = request.GET.get('start')
        end = request.GET.get('end')
        if len(start) == 10 and len(end) == 10:
            xlsx = sapling_report.SaplingReportSheet(user=self.request.user, start=start, end=end)
            return xlsx.generate_sapling_excel_report()
        else:
            messages.error(request, "Sana noto'g'ri kiritilgan")
            return render(request, 'urmon_barpo/sapling/report/regions_and_departments.html', {})


class SproutPlanReportXLSX(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/trees/sprout/report"""

    def get(self, request):
        from .excel import sprouting_report
        start = request.GET.get('start')
        end = request.GET.get('end')
        if start and end:
            xlsx = sprouting_report.SproutReportSheet(user=self.request.user, start=start, end=end)
            return xlsx.generate_sprout_excel_report()
        else:
            messages.error(request, "Sana noto'g'ri kiritilgan")
            return render(request, 'urmon_barpo/sprout/report/regions_and_departments.html', {})


class SaplingInputOutputXLSX(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/trees/sapling/department/in/out/report/6"""

    def get(self, request, department_pk):
        from .excel import sapling_residue_report
        start = request.GET.get('start')
        end = request.GET.get('end')
        if start and end:
            try:
                obj = Department.objects.get(pk=department_pk)
                xlsx = sapling_residue_report.AnnualReportSaplingResidueSheet(start=start, end=end, obj=obj)
                return xlsx.generate_annual_sapling_excel_report()
            except Department.DoesNotExist:
                raise Http404("Given query not found....")
        else:
            messages.error(request, "Sana noto'g'ri kiritilgan")
            return render(request, 'urmon_barpo/sapling/report/input_output_report.html', {})


class SproutInputOutputXLSX(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/trees/sprout/department/in/out/report/7"""

    def get(self, request, department_pk):
        from .excel import sprout_residue_report
        start = request.GET.get('start')
        end = request.GET.get('end')
        if start and end:
            try:
                obj = Department.objects.get(pk=department_pk)
                xlsx = sprout_residue_report.AnnualReportSproutResidueSheet(start=start, end=end, obj=obj)
                return xlsx.generate_annual_sprout_excel_report()
            except Department.DoesNotExist:
                raise Http404("Given query not found....")
        else:
            messages.error(request, "Sana noto'g'ri kiritilgan")
            return render(request, 'urmon_barpo/sprout/report/input_output_report.html', {})


class ForestQuarterPlanReportXLSX(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/trees/land/all/report"""

    def get(self, request):
        from .excel import forest_by_quarter
        start = request.GET.get('start')
        end = request.GET.get('end')
        if start and end and start[:4] == end[:4]:
            xlsx = forest_by_quarter.FinanceReportSheet(user=self.request.user, start=start, end=end)
            return xlsx.generate_finance_excel_report()
        else:
            messages.error(request, "Sana noto'g'ri kiritilgan")
            return render(request, 'urmon_barpo/seed/reports/regions_and_departments.html', {})


class ForestTreeGroundReportXLSX(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/trees/the_ground/regort"""

    def get(self, request):
        from .excel import build_forest
        start = request.GET.get('start')
        end = request.GET.get('end')
        if start and end:
            xlsx = build_forest.ForestTreePlantSheetSheet(user=self.request.user, start=start, end=end)
            return xlsx.generate_forest_excel_report()
        else:
            messages.error(request, "Sana noto'g'ri kiritilgan")
            return render(request, 'urmon_barpo/tree_ground_planting/reports/regions_and_departments.html', {})


class TreeContractReportXLSX(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/trees/tree/contract/report"""

    def get(self, request):
        from .excel.tree_contract import TreeContractReportSheet
        start = request.GET.get('start')
        end = request.GET.get('end')
        if start and end and len(end) == 10:
            xlsx = TreeContractReportSheet(user=self.request.user, start=start, end=end)
            return xlsx.generate_tree_contract_excel_report()
        else:
            messages.error(request, "Sana noto'g'ri kiritilgan")
            return render(request, 'urmon_barpo/tree_contract/reports/region_and_departments.html', {})


class DevelopmentExcelReportView(View):
    """http://127.0.0.1:8000/trees/excel/page"""

    def get(self, request):
        return render(request, 'excel.html', {})


# class GenerateDevelopmentXLSX(View):
#     """http://127.0.0.1:8000/chorvachilik/chorva/in/out/department/report/99"""
#
#     def get(self, request):
#         from ..chorvachilik.excel.chorva_by_type import ChorvaByTypeSheet
#         type_name = request.GET.get('type_name', None)
#         start = request.GET['start']
#         end = request.GET['end']
#         if start and end:
#             try:
#                 if int(type_name) == 4:
#                     from ..chorvachilik.excel.poultry_report import PoultrySheet
#                     obj = ChorvachilikTypes.objects.get(pk=type_name)
#                     xlsx = PoultrySheet(obj=obj, start=start, end=end)
#                     return xlsx.generate_poultry_excel_report()
#                 else:
#                     obj = ChorvachilikTypes.objects.get(pk=type_name)
#                     xlsx = ChorvaByTypeSheet(obj=obj, start=start, end=end)
#                     return xlsx.generate_chorva_by_type_report()
#             except TreeTypes.DoesNotExist:
#                 raise Http404("Given query not found....")
#         else:
#             messages.error(request, "Sana noto'g'ri kiritilgan")
#             return render(request, "chorvachilik/reports/regions_and_departments.html", {})
class GenerateDevelopmentXLSX(View):

    def get(self, request):
        from .excel.tree_contract import TreeContractReportSheet
        start = request.GET.get('start')
        end = request.GET.get('end')
        # at = request.GET['amount_type']
        if start and end:
            xlsx = TreeContractReportSheet(user=self.request.user, start=start, end=end)
            return xlsx.generate_tree_contract_excel_report()
        else:
            messages.error(request, "Sana noto'g'ri kiritilgan")
            return render(request, 'excel.html', {})


def get_sapling_input_output_tree_category_data(department_id=None, start=None, end=None):
    """Ko'chatchilik input output report department uchun daraxtlar categoriyasi"""
    with connection.cursor() as cursor:
        query = f"""
                select tp.category_id, -1, tc.name, (select (coalesce(sum(si.donation),0) + coalesce(sum(si.buying),0) + coalesce(sum(si.new_sprout),0)) -
                (coalesce(sum(so.for_the_forest),0) + coalesce(sum(so.unsuccessful),0)+ coalesce(sum(so.place_changed),0)+ coalesce(sum(so.selling),0) 
									 + coalesce(sum(so.donation),0) + coalesce(sum(so.out_of_count), 0))
                 from tree_plant tp1 left join sapling_input si on si.plant_id = tp1.id and si.date < '{year_start}' and si.department_id = {department_id}
                 left join sapling_output so on so.plant_id = tp1.id and so.date < '{year_start}' and so.department_id = {department_id}
                 where tp1.category_id = tp.category_id) qoldiq,  coalesce(sum(si.donation),0), coalesce(sum(si.buying),0), coalesce(sum(si.new_sprout),0), 
                 (coalesce(sum(si.donation), 0) + coalesce(sum(si.buying),0) + coalesce(sum(si.new_sprout),0)),
                 coalesce(sum(so.for_the_forest),0),  coalesce(sum(so.unsuccessful),0), coalesce(sum(so.place_changed),0),  coalesce(sum(so.selling),0), 
                 coalesce(sum(so.donation),0), coalesce(sum(so.out_of_count),0), 
                 (coalesce(sum(si.donation),0) + coalesce(sum(si.buying),0) + coalesce(sum(si.new_sprout),0)) - 
                 (coalesce(sum(so.for_the_forest),0) + coalesce(sum(so.unsuccessful),0) + coalesce(sum(so.place_changed),0) + coalesce(sum(so.selling),0) 
				  + coalesce(sum(so.donation),0) + coalesce(sum(so.out_of_count),0) )
                 from tree_plant tp
                 left join tree_category tc on tc.id = tp.category_id
                 left join sapling_input si on si.plant_id = tp.id and si.date between '{year_start}' and '{year_end}' and si.department_id = {department_id}
                 left join sapling_output so on so.plant_id = tp.id and so.date between '{year_start}' and '{year_end}' and so.department_id = {department_id}
                 group by tp.category_id, tc.name order by tp.category_id
        """

        cursor.execute(query)
        row = cursor.fetchall()
        return row


def get_department_sapling_input_output_tree_report_data(department_id=None, start=None, end=None):
    """Ko'chatchilik input output report department uchun daraxtlar data si """
    with connection.cursor() as cursor:
        query = f"""
                select tp.category_id,
                tp.id, tp.name, (select (coalesce(sum(si.donation),0) + coalesce(sum(si.buying),0) + coalesce(sum(si.new_sprout),0)) -
                (coalesce(sum(so.for_the_forest),0) + coalesce(sum(so.unsuccessful),0)+ coalesce(sum(so.place_changed),0)+ coalesce(sum(so.selling),0)
                 + coalesce(sum(so.donation),0) + coalesce(sum(so.out_of_count),0))
                from tree_plant tp1 left join sapling_input si on si.plant_id = tp1.id and si.date < '{year_start}' and si.department_id = {department_id}
                left join sapling_output so on so.plant_id = tp1.id and so.date < '{year_start}' and so.department_id = {department_id}
                where tp1.id = tp.id) qoldiq, sum(si.donation) donation, sum(si.buying) buying, sum(si.new_sprout) new_sprout, 
                (sum(si.donation) + sum(si.buying) +sum(si.new_sprout)) jami, 
                sum(so.for_the_forest),  sum(so.unsuccessful), sum(so.place_changed),  sum(so.selling),
                sum(so.donation), sum(so.out_of_count), 
                (coalesce(sum(si.donation),0) + coalesce(sum(si.buying),0) + coalesce(sum(si.new_sprout),0) ) - 
                (coalesce(sum(so.for_the_forest),0) + coalesce(sum(so.unsuccessful),0) + coalesce(sum(so.place_changed),0) + coalesce(sum(so.selling),0) 
                 + coalesce(sum(so.donation),0) + coalesce(sum(so.out_of_count),0))
                from tree_plant tp left join sapling_input si on si.plant_id = tp.id and si.date between '{year_start}' and '{year_end}' and si.department_id = {department_id}
                left join sapling_output so on so.plant_id = tp.id and so.date between '{year_start}' and '{year_end}' and so.department_id = {department_id} 
                group by tp.id, tp.name order by tp.category_id
        """
        cursor.execute(query)
        row = cursor.fetchall()
        return row
