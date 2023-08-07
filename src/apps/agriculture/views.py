import json
from datetime import date, datetime, timedelta
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from .filters import AgricultureActualFilter
from .forms import *
from django_filters.views import FilterView
from django.contrib import messages
from .models import *
from ..core.service import get_current_user_regions_and_departments_json, get_current_user_regions_and_departments_qs
from ..finance.forms import FilterForm
from ..finance.views import generate_month_year, _check_sum_is_none, _calculate_percentage
from ..trees.views import JsonData
from ..report.models import Report as Rp

epoch_year = date.today().year
year_start = date(epoch_year, 1, 1).strftime('%Y-%m-%d')
year_end = date(epoch_year, 12, 31).strftime('%Y-%m-%d')


class AgricultureActualList(LoginRequiredMixin, FilterView, ListView):
    model = AgricultureActual
    context_object_name = 'object_list'
    template_name = 'Agriculture/agriculture_actual/list.html'
    paginate_by = 12
    filterset_class = AgricultureActualFilter

    def get_context_data(self, **kwargs):
        context = super(AgricultureActualList, self).get_context_data(**kwargs)
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        context['department_json'] = departments
        context['region_json'] = regions
        context['department'] = self.request.GET.get('department', '')
        context['region'] = self.request.GET.get('region', '')
        context['amount'] = self.request.GET.get('amount', '')
        context['department_name'] = self.request.GET.get('department_name', None)
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return AgricultureActual.objects.filter(region__in=regions, department__in=departments, status=1).order_by(
                '-id')
        else:
            return AgricultureActual.objects.filter(status=44).order_by('-id')


class AgricultureActualCreate(LoginRequiredMixin, View):
    template_name = 'Agriculture/agriculture_actual/create.html'

    def get(self, request):
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        context = {"departments": departments,
                   "regions": regions,
                   "tree_plants": JsonData().get_json_data(tree_plant=True),
                   "tree_types": JsonData().get_json_data(tree_type=True)}
        return render(request, self.template_name, context)

    def post(self, request):
        data = request.POST
        items = json.loads(data['items'])
        for i in range(len(items)):
            AgricultureActual.objects.create(
                date=data['date'],
                department=Department.objects.get(id=data['department']),
                region=Region.objects.get(id=data['region']),
                hectare=float(items[i]['hectare']),
                weight=float(items[i]['weight']),
                profit=items[i]['profit'],
                yield_area=items[i]['yield_area'],
                show_yield_area=items[i]['show_yield_area'],
                tree_plant=TreePlant.objects.get(id=items[i]['tree_plant']),
                tree_type=TreeTypes.objects.get(id=data['tree_type']),
                creator=self.request.user
            )
        return redirect('agriculture:agriculture_actual_list')


class AgricultureActualDetail(LoginRequiredMixin, View):
    template_name = 'Agriculture/agriculture_actual/detail.html'

    def get(self, request, pk):
        try:
            agriculture = AgricultureActual.objects.get(pk=pk)
            form = AgricultureActualForm(initial={
                'date': agriculture.date,
                "hectare": agriculture.hectare,
                "weight": agriculture.weight,
                "department": agriculture.department,
                "creator": agriculture.creator,
                "profit": agriculture.profit,
                "yield_area": agriculture.yield_area,
                "region": agriculture.region,
                "tree_plant": agriculture.tree_plant,
                "tree_type": agriculture.tree_type,
                "show_yield_area": agriculture.show_yield_area})
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "agriculture": agriculture,
                "data": departments,
                "region": regions,
                "tree_plants": JsonData().get_json_data(tree_plant=True),
                "tree_types": JsonData().get_json_data(tree_type=True),
                'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            agriculture = AgricultureActual.objects.get(pk=pk)
            form = AgricultureActualForm(instance=agriculture, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('agriculture:agriculture_actual_list')
            else:
                return redirect('agriculture:agriculture_actual_list')
        except ObjectDoesNotExist:
            return redirect('agriculture:agriculture_actual_list')


class AgricultureActualDeleteView(LoginRequiredMixin, View):
    template_name = 'Agriculture/agriculture_actual/list.html'

    def get(self, request, pk):
        qs = AgricultureActual.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('agriculture:agriculture_actual_list')
        else:
            return redirect('agriculture:agriculture_actual_list')


class AgriculturePlanList(LoginRequiredMixin, ListView):
    template_name = 'Agriculture/agriculture_plan/list.html'
    paginate_by = 10
    model = AgriculturePlan

    def get_context_data(self, *args, **kwargs):
        context = super(AgriculturePlanList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return AgriculturePlan.objects.filter(region__in=regions, department__in=departments, status=1).order_by(
                '-id')
        else:
            return AgriculturePlan.objects.filter(status=44).order_by('-id')


class AgriculturePlanCreate(LoginRequiredMixin, View):
    template_name = 'Agriculture/agriculture_plan/create.html'

    def get(self, request):
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        context = {"departments": departments,
                   "regions": regions,
                   "tree_plants": JsonData().get_json_data(tree_plant=True),
                   "tree_types": JsonData().get_json_data(tree_type=True)}
        return render(request, self.template_name, context)

    def post(self, request):
        data = request.POST
        print("data", data)
        items = json.loads(data['items'])
        nexxt = json.loads(data['next'])
        for i in range(len(items)):
            AgriculturePlan.objects.create(
                date=data['date'],
                department=Department.objects.get(id=data['department']),
                region=Region.objects.get(id=data['region']),
                tree_plant=TreePlant.objects.get(id=items[i]['tree_plant']),
                tree_type=TreeTypes.objects.get(id=items[i]['tree_type']),
                hectare=items[i]['hectares'],
                weight=items[i]['weights'],
                creator=self.request.user
            )
        if nexxt:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            ctx = {"departments": departments,
                   "regions": regions,
                   "tree_plants": JsonData().get_json_data(tree_plant=True),
                   "tree_types": JsonData().get_json_data(tree_type=True),
                   "msg": "Success"
                   }
            return render(request, self.template_name, ctx)
        else:
            return redirect('agriculture:agriculture_plan_list')


class AgriculturePlanDetail(LoginRequiredMixin, View):
    template_name = 'Agriculture/agriculture_plan/detail.html'

    def get(self, request, pk):
        try:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            agriculture = AgriculturePlan.objects.get(pk=pk)
            # print(agriculture.tree_type)
            # tree_plant = serialize('json', TreePlant.objects.filter(types=agriculture.tree_type))
            # print("tree_plant", tree_plant)
            form = AgriculturePlanForm(initial={
                'date': agriculture.date,
                "hectare": agriculture.hectare,
                "weight": agriculture.weight,
                "department": agriculture.department,
                "creator": agriculture.creator,
                "region": agriculture.region,
                "tree_type": agriculture.tree_type,
                "tree_plant": agriculture.tree_plant})
            context = {
                "is_user": True,
                "agriculture": agriculture,
                "data": departments,
                "region": regions,
                "tree_plants": JsonData().get_json_data(tree_plant=True),
                "tree_types": JsonData().get_json_data(tree_type=True),
                'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            print('request.POST', request.POST)
            agriculture = AgriculturePlan.objects.get(pk=pk)
            form = AgriculturePlanForm(instance=agriculture, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('agriculture:agriculture_plan_list')
            else:
                return redirect('agriculture:agriculture_plan_list')
        except ObjectDoesNotExist:
            return redirect('agriculture:agriculture_plan_list')


class AgriculturePlanDeleteView(LoginRequiredMixin, View):
    template_name = 'Agriculture/agriculture_plan/list.html'

    def get(self, request, pk):
        qs = AgriculturePlan.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('agriculture:agriculture_plan_list')
        else:
            return redirect('agriculture:agriculture_plan_list')


class AgricultureReportDashboardView(LoginRequiredMixin, View):
    template_name = "Agriculture/reports/dashboard.html"

    def get(self, request):
        data = Rp.objects.filter(type=4, status=1)
        tree_type = TreeTypes.objects.filter(status=1).first().id
        ctx = {"start": year_start, "end": year_end,
               "type": tree_type,
               "data": data, "current_year": date.today().year}
        return render(request, self.template_name, ctx)


class AgricultureAllReportView(LoginRequiredMixin, View):
    template_name = "Agriculture/reports/barcha_hisobot.html"

    def get(self, request):
        tipp = self.request.GET.get('type', None)
        epoch_year = date.today().year
        end_date = date(epoch_year, 12, 31)
        year_end = self.request.GET.get('end', None)
        if not year_end:
            end_dateformat = end_date
            epoch_year = end_dateformat.year
            year_start = date(epoch_year, 1, 1).strftime('%Y-%m-%d')
            year_end = date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.strptime(year_end, '%Y-%m-%d')
            epoch_year = end_dateformat.year
            year_start = date(epoch_year, 1, 1).strftime('%Y-%m-%d')
            year_end = end_dateformat.strftime('%Y-%m-%d')
        form = FilterForm(initial={"start": year_start, "end": year_end})
        all_hectare_plan_sum = 0
        all_weight_plan_sum = 0
        all_cent_plan_sum = 0
        all_hectare_actual_sum = 0
        all_weight_actual_sum = 0
        all_cent_actual_sum = 0
        agricul_actual_data = None
        agricul_plan_data = None
        data = []
        sum_tree_plan_data = []
        sum_tree_actual_data = []
        sum_tree_percentage_data = []
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and tipp:
            agriculture_actual_data = AgricultureActual.objects.filter(region__in=regions, date__year=epoch_year,
                                                                       tree_type=tipp, status=1)
            agriculture_plan_data = AgriculturePlan.objects.filter(region__in=regions, department__in=departments,
                                                                   date__range=[year_start, year_end],
                                                                   tree_type=tipp,
                                                                   status=1)
            tree_type = TreeTypes.objects.filter(id=tipp).first()
            plants_data = TreePlant.objects.filter(types=tipp)
            for plant in plants_data:
                # Shu daraxtdan jami reja va amaldagi hectare, weight, centner olyabmiz
                # PLAN
                sum_tree_plan_hectare_qs = agriculture_plan_data.filter(tree_plant=plant).aggregate(
                    Sum('hectare'))
                sum_tree_plan_weight_qs = agriculture_plan_data.filter(tree_plant=plant).aggregate(
                    Sum('weight'))
                sum_tree_plan_hectare = _check_sum_is_none(sum_tree_plan_hectare_qs['hectare__sum'])
                sum_tree_plan_weight = _check_sum_is_none(sum_tree_plan_weight_qs['weight__sum'])
                sum_plant_cent_actual = 0
                if sum_tree_plan_hectare and sum_tree_plan_weight:
                    sum_plant_cent_actual = sum_tree_plan_weight * 10 / sum_tree_plan_hectare

                sum_tree_plan_data.append({
                    "sum_tree_plan_hectare": sum_tree_plan_hectare,
                    "sum_tree_plan_weight": sum_tree_plan_weight,
                    "sum_plant_cent_actual": sum_plant_cent_actual,
                })
                # ACTUAL
                sum_tree_actual_hectare_qs = agriculture_actual_data.filter(tree_plant=plant).aggregate(
                    Sum('hectare'))
                sum_tree_actual_weight_qs = agriculture_actual_data.filter(tree_plant=plant).aggregate(
                    Sum('weight'))
                sum_tree_actual_hectare = _check_sum_is_none(sum_tree_actual_hectare_qs['hectare__sum'])
                sum_tree_actual_weight = _check_sum_is_none(sum_tree_actual_weight_qs['weight__sum'])
                sum_actual_cent_actual = 0
                if sum_tree_actual_hectare and sum_tree_actual_weight:
                    sum_actual_cent_actual = sum_tree_actual_weight * 10 / sum_tree_actual_hectare
                sum_tree_actual_data.append({
                    "sum_tree_actual_hectare": sum_tree_actual_hectare,
                    "sum_tree_actual_weight": sum_tree_actual_weight,
                    "sum_actual_cent_actual": sum_actual_cent_actual
                })
                # PERCENTAGE
                sum_tree_percentage_data.append({
                    "sum_tree_hectare_percentage": _calculate_percentage(sum_tree_plan_hectare,
                                                                         sum_tree_actual_hectare),
                    "sum_tree_weight_percentage": _calculate_percentage(sum_tree_plan_weight, sum_tree_actual_weight),
                    "sum_tree_cent_percentage": _calculate_percentage(sum_plant_cent_actual, sum_actual_cent_actual)
                })
            for region in regions:
                first = []
                second = []
                three = []
                for plant in plants_data:
                    # PLAN
                    plant_hectare_plan_query = agriculture_plan_data.filter(tree_plant=plant, region=region).aggregate(
                        Sum('hectare'))
                    plant_weight_plan_query = agriculture_plan_data.filter(tree_plant=plant, region=region).aggregate(
                        Sum('weight'))
                    plant_hectare_plan = _check_sum_is_none(plant_hectare_plan_query['hectare__sum'])
                    plant_weight_plan = _check_sum_is_none(plant_weight_plan_query['weight__sum'])
                    plant_cent_plan = 0
                    if plant_weight_plan and plant_hectare_plan:
                        plant_cent_plan = plant_weight_plan * 10 / plant_hectare_plan
                    # ACTUAL
                    plant_hectare_actual_query = agriculture_actual_data.filter(tree_plant=plant,
                                                                                region=region).aggregate(
                        Sum('hectare'))
                    plant_weight_actual_query = agriculture_actual_data.filter(tree_plant=plant,
                                                                               region=region).aggregate(
                        Sum('weight'))
                    plant_hectare_actual = _check_sum_is_none(plant_hectare_actual_query['hectare__sum'])
                    plant_weight_actual = _check_sum_is_none(plant_weight_actual_query['weight__sum'])
                    plant_actual_profit_query = agriculture_actual_data.filter(tree_plant=plant,
                                                                               region=region).aggregate(
                        (Sum('profit')))
                    plant_actual_yield_area_query = agriculture_actual_data.filter(tree_plant=plant,
                                                                                   region=region).aggregate(
                        (Sum('yield_area')))
                    plant_actual_profit = _check_sum_is_none(plant_actual_profit_query['profit__sum'])
                    plant_actual_yield_area = _check_sum_is_none(plant_actual_yield_area_query['yield_area__sum'])
                    plant_cent_actual = 0
                    if plant_weight_actual and plant_hectare_actual:
                        plant_cent_actual = plant_weight_actual * 10 / plant_hectare_actual
                    plant_hectare_percentage = _calculate_percentage(plant_hectare_plan, plant_hectare_actual)
                    plant_weight_percentage = _calculate_percentage(plant_weight_plan, plant_weight_actual)
                    plant_cent_percentage = _calculate_percentage(plant_cent_plan, plant_cent_actual)
                    first.append({
                        "plant_plan_hectare": plant_hectare_plan,
                        "plant_plan_cent": plant_cent_plan,
                        "plant_plan_weight": plant_weight_plan,
                    })
                    second.append({
                        "plant_actual_hectare": plant_hectare_actual,
                        "plant_actual_cent": plant_cent_actual,
                        "plant_actual_weight": plant_weight_actual,
                    })
                    three.append({
                        "plant_hectare_percentage": plant_hectare_percentage,
                        "plant_cent_percentage": plant_cent_percentage,
                        "plant_weight_percentage": plant_weight_percentage
                    })

                # PLAN
                region_hectare_plan_query = agriculture_plan_data.filter(region=region).aggregate(Sum('hectare'))
                region_weight_plan_query = agriculture_plan_data.filter(region=region).aggregate(Sum('weight'))
                region_hectare_plan = _check_sum_is_none(region_hectare_plan_query['hectare__sum'])
                region_weight_plan = _check_sum_is_none(region_weight_plan_query['weight__sum'])
                region_cent_plan = 0
                if region_hectare_plan and region_weight_plan:
                    region_cent_plan = region_weight_plan * 10 / region_hectare_plan
                all_hectare_plan_sum += region_hectare_plan
                all_weight_plan_sum += region_weight_plan
                all_cent_plan_sum += region_cent_plan
                # ACTUAL
                region_hectare_actual_query = agriculture_actual_data.filter(region=region).aggregate(Sum('hectare'))
                region_weight_actual_query = agriculture_actual_data.filter(region=region).aggregate(Sum('weight'))
                region_hectare_actual = _check_sum_is_none(region_hectare_actual_query['hectare__sum'])
                region_weight_actual = _check_sum_is_none(region_weight_actual_query['weight__sum'])
                region_cent_actual = 0
                if region_hectare_actual and region_weight_actual:
                    region_cent_actual = region_weight_actual * 10 / region_hectare_actual

                all_hectare_actual_sum += region_hectare_actual
                all_weight_actual_sum += region_weight_actual
                all_cent_actual_sum += region_cent_actual

                region_profit_actual_query = agriculture_actual_data.filter(region=region).aggregate(Sum('profit'))
                region_yield_area_actual_query = agriculture_actual_data.aggregate(Sum('yield_area'))

                region_profit_actual = _check_sum_is_none(region_profit_actual_query['profit__sum'])
                region_yield_area = _check_sum_is_none(region_yield_area_actual_query['yield_area__sum'])
                region_hectare_percentage = _calculate_percentage(region_hectare_plan, region_hectare_actual)
                region_cent_percentage = _calculate_percentage(region_cent_plan, region_cent_actual)
                region_weight_percentage = _calculate_percentage(region_weight_plan, region_weight_actual)
                data.append({
                    "region_id": region.id,
                    "region_name": region.name,
                    "region_plan_hectare": region_hectare_plan,
                    "region_plan_cent": region_cent_plan,
                    "region_plan_weight": region_weight_plan,
                    "region_actual_hectare": region_hectare_actual,
                    "region_profit_actual": region_profit_actual,
                    "region_actual_cent": region_cent_actual,
                    "region_yield_area": region_yield_area,
                    "region_actual_weight": region_weight_actual,
                    "region_hectare_percentage": region_hectare_percentage,
                    "region_cent_percentage": region_cent_percentage,
                    "region_weight_percentage": region_weight_percentage,
                    "first_line": first,
                    "second_line": second,
                    "three_line": three
                })
            all_profit_sum_query = agriculture_actual_data.aggregate(Sum('profit'))
            all_yield_area_sum_query = agriculture_actual_data.aggregate(Sum('yield_area'))

            all_profit_sum = _check_sum_is_none(all_profit_sum_query['profit__sum'])
            all_yield_area_sum = _check_sum_is_none(all_yield_area_sum_query['yield_area__sum'])
            all_hectare_percentage = _calculate_percentage(all_hectare_plan_sum, all_hectare_actual_sum)
            all_cent_percentage = _calculate_percentage(all_cent_plan_sum, all_cent_actual_sum)
            all_weight_percentage = _calculate_percentage(all_weight_plan_sum, all_weight_actual_sum)

            all_sum = {"all_hectare_plan_sum": all_hectare_plan_sum,
                       "all_weight_plan_sum": all_weight_plan_sum,
                       "all_cent_plan_sum": all_cent_plan_sum,
                       "all_hectare_actual_sum": all_hectare_actual_sum,
                       "all_weight_actual_sum": all_weight_actual_sum,
                       "all_cent_actual_sum": all_cent_actual_sum,
                       "all_hectare_percentage": all_hectare_percentage,
                       "all_cent_percentage": all_cent_percentage,
                       "all_profit_sum": all_profit_sum,
                       "all_yield_area_sum": all_yield_area_sum,
                       "all_weight_percentage": all_weight_percentage}
            context = {"tree_type": tree_type,
                       "form": form, "all_sum": all_sum,
                       "data": data, "start": year_start,
                       "plants_data": plants_data,
                       "sum_tree_plan_data": sum_tree_plan_data,
                       "sum_tree_actual_data": sum_tree_actual_data,
                       "sum_tree_percentage_data": sum_tree_percentage_data,
                       "end": year_end, "tipp": tipp}
            return render(request, self.template_name, context)
        else:
            context = {"form": form, "start": year_start, "end": year_end, "tipp": tipp}
            return render(request, self.template_name, context)


class AgricultureOnlyAllReportView(LoginRequiredMixin, View):
    template_name = "Agriculture/reports/only_all_report_page.html"

    def get(self, request):
        tipp = self.request.GET.get('type', None)
        epoch_year = date.today().year
        end_date = date(epoch_year, 12, 31)
        year_end = self.request.GET.get('end', None)
        if not year_end:
            end_dateformat = end_date
            epoch_year = end_dateformat.year
            year_start = date(epoch_year, 1, 1).strftime('%Y-%m-%d')
            year_end = date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.strptime(year_end, '%Y-%m-%d')
            epoch_year = end_dateformat.year
            year_start = date(epoch_year, 1, 1).strftime('%Y-%m-%d')
            year_end = end_dateformat.strftime('%Y-%m-%d')
        form = FilterForm(initial={"start": year_start, "end": year_end})
        show_profit = False
        region_obj = None
        region_id = None
        all_hectare_plan_sum = 0
        all_weight_plan_sum = 0
        all_cent_plan_sum = 0
        all_hectare_actual_sum = 0
        all_weight_actual_sum = 0
        all_cent_actual_sum = 0
        agricul_actual_data = None
        agricul_plan_data = None
        data = []
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments and tipp:
            if tipp == "all":
                agricul_actual_data = AgricultureActual.objects.filter(region__in=regions, department__in=departments,
                                                                       date__year=epoch_year, status=1).exclude(
                    tree_type=17)
                agricul_plan_data = AgriculturePlan.objects.filter(region__in=regions, department__in=departments,
                                                                   date__range=[year_start, year_end],
                                                                   status=1).exclude(tree_type=17)
            elif tipp != "all":
                show_profit = TreeTypes.objects.filter(id=tipp)[0].show_profit
                agricul_actual_data = AgricultureActual.objects.filter(region__in=regions, department__in=departments,
                                                                       date__year=epoch_year, tree_type=tipp, status=1)
                agricul_plan_data = AgriculturePlan.objects.filter(region__in=regions, department__in=departments,
                                                                   date__range=[year_start, year_end], tree_type=tipp,
                                                                   status=1)
            x = 1
            for department in departments:
                x = x + 1
                # PLAN
                depart_plan_hectare_query = agricul_plan_data.filter(department=department).aggregate(Sum('hectare'))
                depart_plan_weight_query = agricul_plan_data.filter(department=department).aggregate(Sum('weight'))

                depart_plan_hectare = _check_sum_is_none(depart_plan_hectare_query['hectare__sum'])
                depart_plan_weight = _check_sum_is_none(depart_plan_weight_query['weight__sum'])

                depart_plan_cent = 0
                if depart_plan_hectare and depart_plan_weight:
                    depart_plan_cent = depart_plan_weight * 10 / depart_plan_hectare
                # amalda
                depart_actual_profit_query = agricul_actual_data.filter(department=department).aggregate(
                    (Sum('profit')))
                depart_actual_yield_area_query = agricul_actual_data.filter(department=department).aggregate(
                    (Sum('yield_area')))
                depart_actual_hectare_query = agricul_actual_data.filter(department=department).aggregate(
                    Sum('hectare'))
                depart_actual_weight_query = agricul_actual_data.filter(department=department).aggregate(Sum('weight'))

                depart_actual_profit = _check_sum_is_none(depart_actual_profit_query['profit__sum'])
                depart_actual_yield_area = _check_sum_is_none(depart_actual_yield_area_query['yield_area__sum'])
                depart_actual_hectare = _check_sum_is_none(depart_actual_hectare_query['hectare__sum'])
                depart_actual_weight = _check_sum_is_none(depart_actual_weight_query['weight__sum'])
                depart_actual_cent = 0
                if depart_actual_hectare and depart_actual_weight:
                    depart_actual_cent = depart_actual_weight * 10 / depart_actual_hectare
                depart_hectare_percentage = _calculate_percentage(depart_plan_hectare, depart_actual_hectare)
                depart_cent_percentage = _calculate_percentage(depart_plan_cent, depart_actual_cent)
                depart_weight_percentage = _calculate_percentage(depart_plan_weight, depart_actual_weight)
                if region_id != department.region_id:
                    region_obj = Region.objects.get(id=department.region_id)
                    # PLAN
                    region_plan_hectare_query = agricul_plan_data.filter(region=region_obj,
                                                                         department__in=departments).aggregate(
                        Sum('hectare'))
                    region_plan_weight_query = agricul_plan_data.filter(region=region_obj,
                                                                        department__in=departments).aggregate(
                        Sum('weight'))

                    region_plan_hectare = _check_sum_is_none(region_plan_hectare_query['hectare__sum'])
                    region_plan_weight = _check_sum_is_none(region_plan_weight_query['weight__sum'])
                    region_plan_cent = 0
                    if region_plan_hectare and region_plan_weight:
                        region_plan_cent = region_plan_weight * 10 / region_plan_hectare

                    # AMALDA
                    region_actual_hectare_query = agricul_actual_data.filter(region=region_obj,
                                                                             department__in=departments).aggregate(
                        Sum('hectare'))
                    region_actual_weight_query = agricul_actual_data.filter(region=region_obj,
                                                                            department__in=departments).aggregate(
                        Sum('weight'))
                    region_actual_profit_query = agricul_actual_data.filter(region=region_obj,
                                                                            department__in=departments).aggregate(
                        Sum('profit'))
                    region_actual_yield_area_query = agricul_actual_data.filter(region=region_obj,
                                                                                department__in=departments).aggregate(
                        Sum('yield_area'))

                    region_actual_yield_area = _check_sum_is_none(region_actual_yield_area_query['yield_area__sum'])
                    region_actual_profit = _check_sum_is_none(region_actual_profit_query['profit__sum'])
                    region_actual_hectare = _check_sum_is_none(region_actual_hectare_query['hectare__sum'])
                    region_actual_weight = _check_sum_is_none(region_actual_weight_query['weight__sum'])
                    region_actual_cent = 0
                    if region_actual_hectare and region_actual_weight:
                        region_actual_cent = region_actual_weight * 10 / region_actual_hectare

                    region_hectare_percentage = _calculate_percentage(region_plan_hectare, region_actual_hectare)
                    region_weight_percentage = _calculate_percentage(region_plan_weight, region_actual_weight)
                    region_cent_percentage = _calculate_percentage(region_plan_cent, region_actual_cent)
                    all_hectare_plan_sum += region_plan_hectare
                    all_weight_plan_sum += region_plan_weight
                    if region_plan_weight and region_plan_hectare:
                        all_cent_plan_sum += region_plan_weight * 10 / region_plan_hectare

                    all_hectare_actual_sum += region_actual_hectare
                    all_weight_actual_sum += region_actual_weight
                    if region_actual_weight and region_actual_hectare:
                        all_cent_actual_sum += region_actual_weight * 10 / region_actual_hectare
                    data.append({
                        "index": 1,
                        "region_id": region_obj.id,
                        "region_name": region_obj.name,
                        "region_plan_hectare": region_plan_hectare,
                        "region_plan_cent": region_plan_cent,
                        "region_plan_weight": region_plan_weight,
                        "region_actual_hectare": region_actual_hectare,
                        "region_actual_yield_area": region_actual_yield_area,
                        "region_actual_cent": region_actual_cent,
                        "region_actual_weight": region_actual_weight,
                        "region_actual_profit": region_actual_profit,
                        "region_hectare_percentage": region_hectare_percentage,
                        "region_cent_percentage": region_cent_percentage,
                        "region_weight_percentage": region_weight_percentage,

                        "department_id": department.id,
                        "department_name": department.name,
                        "department_plan_hectare": depart_plan_hectare,
                        "department_plan_cent": depart_plan_cent,
                        "department_plan_weight": depart_plan_weight,
                        "department_actual_hectare": depart_actual_hectare,
                        "department_actual_yield_area": depart_actual_yield_area,
                        "department_actual_cent": depart_actual_cent,
                        "department_actual_weight": depart_actual_weight,
                        "department_actual_profit": depart_actual_profit,
                        "department_hectare_percentage": depart_hectare_percentage,
                        "department_cent_percentage": depart_cent_percentage,
                        "department_weight_percentage": depart_weight_percentage,
                    })
                    x = 1
                else:
                    data.append({
                        "index": x,
                        "department_id": department.id,
                        "department_name": department.name,
                        "department_plan_hectare": depart_plan_hectare,
                        "department_plan_cent": depart_plan_cent,
                        "department_plan_weight": depart_plan_weight,
                        "department_actual_hectare": depart_actual_hectare,
                        "department_actual_yield_area": depart_actual_yield_area,
                        "department_actual_cent": depart_actual_cent,
                        "department_actual_weight": depart_actual_weight,
                        "department_actual_profit": depart_actual_profit,
                        "department_hectare_percentage": depart_hectare_percentage,
                        "department_cent_percentage": depart_cent_percentage,
                        "department_weight_percentage": depart_weight_percentage,
                    })
                region_obj = None
                region_id = department.region_id
            all_profit_sum_query = agricul_actual_data.aggregate(Sum('profit'))
            all_yield_area_sum_query = agricul_actual_data.aggregate(Sum('yield_area'))

            all_profit_sum = _check_sum_is_none(all_profit_sum_query['profit__sum'])
            all_yield_area_sum = _check_sum_is_none(all_yield_area_sum_query['yield_area__sum'])
            all_hectare_percentage = _calculate_percentage(all_hectare_plan_sum, all_hectare_actual_sum)
            all_cent_percentage = _calculate_percentage(all_cent_plan_sum, all_cent_actual_sum)
            all_weight_percentage = _calculate_percentage(all_weight_plan_sum, all_weight_actual_sum)

            all_sum = {"all_hectare_plan_sum": all_hectare_plan_sum,
                       "all_weight_plan_sum": all_weight_plan_sum,
                       "all_cent_plan_sum": all_cent_plan_sum,
                       "all_hectare_actual_sum": all_hectare_actual_sum,
                       "all_weight_actual_sum": all_weight_actual_sum,
                       "all_cent_actual_sum": all_cent_actual_sum,
                       "all_hectare_percentage": all_hectare_percentage,
                       "all_cent_percentage": all_cent_percentage,
                       "all_profit_sum": all_profit_sum,
                       "all_yield_area_sum": all_yield_area_sum,
                       "all_weight_percentage": all_weight_percentage}
            context = {"tree_types": JsonData().get_json_data(tree_type=True),
                       "form": form, "all_sum": all_sum,
                       "data": data, "start": year_start,
                       "end": year_end, "tipp": tipp, "show_profit": show_profit}
            return render(request, self.template_name, context)
        else:
            context = {"tree_types": JsonData().get_json_data(tree_type=True),
                       "form": form, "start": year_start,
                       "end": year_end, "tipp": tipp, "show_profit": show_profit}
            return render(request, self.template_name, context)


class AgricultureRegionReport(LoginRequiredMixin, View):
    template_name = "Agriculture/reports/region.html"

    def get(self, request, pk):
        tipp = self.request.GET.get('type', None)
        epoch_year = date.today().year
        end_date = date(epoch_year, 12, 31)
        year_end = self.request.GET.get('end', None)
        if not year_end:
            end_dateformat = end_date
            epoch_year = end_dateformat.year
            year_start = date(epoch_year, 1, 1).strftime('%Y-%m-%d')
            year_end = date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.strptime(year_end, '%Y-%m-%d')
            epoch_year = end_dateformat.year
            year_start = date(epoch_year, 1, 1).strftime('%Y-%m-%d')
            year_end = end_dateformat.strftime('%Y-%m-%d')
        form = FilterForm(initial={"start": year_start, "end": year_end})
        all_hectare_plan_sum = 0
        all_weight_plan_sum = 0
        all_cent_plan_sum = 0
        all_hectare_actual_sum = 0
        all_weight_actual_sum = 0
        all_cent_actual_sum = 0
        agricul_actual_data = None
        agricul_plan_data = None
        data = []
        sum_tree_plan_data = []
        sum_tree_actual_data = []
        sum_tree_percentage_data = []
        agriculture_actual_data = None
        agriculture_plan_data = None
        tree_type = None
        plants_data = None
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if tipp == 'all':
            agriculture_actual_data = AgricultureActual.objects.filter(region__in=regions, date__year=epoch_year,
                                                                       status=1).exclude(tree_type=17)
            agriculture_plan_data = AgriculturePlan.objects.filter(region__in=regions, department__in=departments,
                                                                   date__range=[year_start, year_end],
                                                                   status=1).exclude(tree_type=17)
            tree_type = TreeTypes.objects.all().exclude(id=17)
            plants_data = TreePlant.objects.filter(types__in=tree_type)
        elif departments and tipp:
            agriculture_actual_data = AgricultureActual.objects.filter(region__in=regions, date__year=epoch_year,
                                                                       tree_type=tipp, status=1)
            agriculture_plan_data = AgriculturePlan.objects.filter(region__in=regions, department__in=departments,
                                                                   date__range=[year_start, year_end],
                                                                   tree_type=tipp,
                                                                   status=1)
            tree_type = TreeTypes.objects.filter(id=tipp).first()
            plants_data = TreePlant.objects.filter(types=tipp)
        else:
            context = {"tree_types": JsonData().get_json_data(tree_type=True),
                       "form": form, "start": year_start,
                       "end": year_end, "tipp": tipp}
            return render(request, self.template_name, context)
        region = Region.objects.get(id=pk)

        for plant in plants_data:
            # Shu daraxtdan jami reja va amaldagi hectare, weight, centner olyabmiz
            # PLAN
            sum_tree_plan_hectare_qs = agriculture_plan_data.filter(tree_plant=plant, region=region).aggregate(
                Sum('hectare'))
            sum_tree_plan_weight_qs = agriculture_plan_data.filter(tree_plant=plant, region=region).aggregate(
                Sum('weight'))
            sum_tree_plan_hectare = _check_sum_is_none(sum_tree_plan_hectare_qs['hectare__sum'])
            sum_tree_plan_weight = _check_sum_is_none(sum_tree_plan_weight_qs['weight__sum'])
            sum_plant_cent_actual = 0
            if sum_tree_plan_hectare and sum_tree_plan_weight:
                sum_plant_cent_actual = sum_tree_plan_weight * 10 / sum_tree_plan_hectare

            sum_tree_plan_data.append({
                "sum_tree_plan_hectare": sum_tree_plan_hectare,
                "sum_tree_plan_weight": sum_tree_plan_weight,
                "sum_plant_cent_actual": sum_plant_cent_actual,
            })
            # ACTUAL
            sum_tree_actual_hectare_qs = agriculture_actual_data.filter(tree_plant=plant, region=region).aggregate(
                Sum('hectare'))
            sum_tree_actual_weight_qs = agriculture_actual_data.filter(tree_plant=plant, region=region).aggregate(
                Sum('weight'))
            sum_tree_actual_hectare = _check_sum_is_none(sum_tree_actual_hectare_qs['hectare__sum'])
            sum_tree_actual_weight = _check_sum_is_none(sum_tree_actual_weight_qs['weight__sum'])
            sum_actual_cent_actual = 0
            if sum_tree_actual_hectare and sum_tree_actual_weight:
                sum_actual_cent_actual = sum_tree_actual_weight * 10 / sum_tree_actual_hectare
            sum_tree_actual_data.append({
                "sum_tree_actual_hectare": sum_tree_actual_hectare,
                "sum_tree_actual_weight": sum_tree_actual_weight,
                "sum_actual_cent_actual": sum_actual_cent_actual
            })
            # PERCENTAGE
            sum_tree_percentage_data.append({
                "sum_tree_hectare_percentage": _calculate_percentage(sum_tree_plan_hectare,
                                                                     sum_tree_actual_hectare),
                "sum_tree_weight_percentage": _calculate_percentage(sum_tree_plan_weight, sum_tree_actual_weight),
                "sum_tree_cent_percentage": _calculate_percentage(sum_plant_cent_actual, sum_actual_cent_actual)
            })
        departments = departments.filter(region=region)
        for department in departments:
            first = []
            second = []
            three = []
            for plant in plants_data:
                # PLAN
                plant_hectare_plan_query = agriculture_plan_data.filter(tree_plant=plant,
                                                                        department=department).aggregate(
                    Sum('hectare'))
                plant_weight_plan_query = agriculture_plan_data.filter(tree_plant=plant,
                                                                       department=department).aggregate(
                    Sum('weight'))
                plant_hectare_plan = _check_sum_is_none(plant_hectare_plan_query['hectare__sum'])
                plant_weight_plan = _check_sum_is_none(plant_weight_plan_query['weight__sum'])
                plant_cent_plan = 0
                if plant_weight_plan and plant_hectare_plan:
                    plant_cent_plan = plant_weight_plan * 10 / plant_hectare_plan
                # ACTUAL
                plant_hectare_actual_query = agriculture_actual_data.filter(tree_plant=plant,
                                                                            department=department).aggregate(
                    Sum('hectare'))
                plant_weight_actual_query = agriculture_actual_data.filter(tree_plant=plant,
                                                                           department=department).aggregate(
                    Sum('weight'))
                plant_hectare_actual = _check_sum_is_none(plant_hectare_actual_query['hectare__sum'])
                plant_weight_actual = _check_sum_is_none(plant_weight_actual_query['weight__sum'])
                plant_actual_profit_query = agriculture_actual_data.filter(tree_plant=plant,
                                                                           department=department).aggregate(
                    (Sum('profit')))
                plant_actual_yield_area_query = agriculture_actual_data.filter(tree_plant=plant,
                                                                               department=department).aggregate(
                    (Sum('yield_area')))
                plant_actual_profit = _check_sum_is_none(plant_actual_profit_query['profit__sum'])
                plant_actual_yield_area = _check_sum_is_none(plant_actual_yield_area_query['yield_area__sum'])
                plant_cent_actual = 0
                if plant_weight_actual and plant_hectare_actual:
                    plant_cent_actual = plant_weight_actual * 10 / plant_hectare_actual
                plant_hectare_percentage = _calculate_percentage(plant_hectare_plan, plant_hectare_actual)
                plant_weight_percentage = _calculate_percentage(plant_weight_plan, plant_weight_actual)
                plant_cent_percentage = _calculate_percentage(plant_cent_plan, plant_cent_actual)
                first.append({
                    "plant_plan_hectare": plant_hectare_plan,
                    "plant_plan_cent": plant_cent_plan,
                    "plant_plan_weight": plant_weight_plan,
                })
                second.append({
                    "plant_actual_hectare": plant_hectare_actual,
                    "plant_actual_cent": plant_cent_actual,
                    "plant_actual_weight": plant_weight_actual,
                })
                three.append({
                    "plant_hectare_percentage": plant_hectare_percentage,
                    "plant_cent_percentage": plant_cent_percentage,
                    "plant_weight_percentage": plant_weight_percentage
                })

            # PLAN
            region_hectare_plan_query = agriculture_plan_data.filter(department=department).aggregate(
                Sum('hectare'))
            region_weight_plan_query = agriculture_plan_data.filter(department=department).aggregate(Sum('weight'))
            region_hectare_plan = _check_sum_is_none(region_hectare_plan_query['hectare__sum'])
            region_weight_plan = _check_sum_is_none(region_weight_plan_query['weight__sum'])
            region_cent_plan = 0
            if region_hectare_plan and region_weight_plan:
                region_cent_plan = region_weight_plan * 10 / region_hectare_plan

            all_hectare_plan_sum += region_hectare_plan
            all_weight_plan_sum += region_weight_plan
            all_cent_plan_sum += region_cent_plan

            # ACTUAL
            region_hectare_actual_query = agriculture_actual_data.filter(department=department).aggregate(
                Sum('hectare'))
            region_weight_actual_query = agriculture_actual_data.filter(department=department).aggregate(
                Sum('weight'))
            region_hectare_actual = _check_sum_is_none(region_hectare_actual_query['hectare__sum'])
            region_weight_actual = _check_sum_is_none(region_weight_actual_query['weight__sum'])
            region_cent_actual = 0
            if region_hectare_actual and region_weight_actual:
                region_cent_actual = region_weight_actual * 10 / region_hectare_actual

            all_hectare_actual_sum += region_hectare_actual
            all_weight_actual_sum += region_weight_actual
            all_cent_actual_sum += region_cent_actual

            region_profit_actual_query = agriculture_actual_data.filter(department=department).aggregate(
                Sum('profit'))
            region_yield_area_actual_query = agriculture_actual_data.aggregate(Sum('yield_area'))

            region_profit_actual = _check_sum_is_none(region_profit_actual_query['profit__sum'])
            region_yield_area = _check_sum_is_none(region_yield_area_actual_query['yield_area__sum'])
            region_hectare_percentage = _calculate_percentage(region_hectare_plan, region_hectare_actual)
            region_cent_percentage = _calculate_percentage(region_cent_plan, region_cent_actual)
            region_weight_percentage = _calculate_percentage(region_weight_plan, region_weight_actual)
            data.append({
                "region_id": department.id,
                "region_name": department.name,
                "region_plan_hectare": region_hectare_plan,
                "region_plan_cent": region_cent_plan,
                "region_plan_weight": region_weight_plan,
                "region_actual_hectare": region_hectare_actual,
                "region_profit_actual": region_profit_actual,
                "region_actual_cent": region_cent_actual,
                "region_yield_area": region_yield_area,
                "region_actual_weight": region_weight_actual,
                "region_hectare_percentage": region_hectare_percentage,
                "region_cent_percentage": region_cent_percentage,
                "region_weight_percentage": region_weight_percentage,
                "first_line": first,
                "second_line": second,
                "three_line": three
            })
        all_profit_sum_query = agriculture_actual_data.filter(region=region).aggregate(Sum('profit'))
        all_yield_area_sum_query = agriculture_actual_data.filter(region=region).aggregate(Sum('yield_area'))

        all_profit_sum = _check_sum_is_none(all_profit_sum_query['profit__sum'])
        all_yield_area_sum = _check_sum_is_none(all_yield_area_sum_query['yield_area__sum'])
        all_hectare_percentage = _calculate_percentage(all_hectare_plan_sum, all_hectare_actual_sum)
        all_cent_percentage = _calculate_percentage(all_cent_plan_sum, all_cent_actual_sum)
        all_weight_percentage = _calculate_percentage(all_weight_plan_sum, all_weight_actual_sum)

        all_sum = {"all_hectare_plan_sum": all_hectare_plan_sum,
                   "all_weight_plan_sum": all_weight_plan_sum,
                   "all_cent_plan_sum": all_cent_plan_sum,
                   "all_hectare_actual_sum": all_hectare_actual_sum,
                   "all_weight_actual_sum": all_weight_actual_sum,
                   "all_cent_actual_sum": all_cent_actual_sum,
                   "all_hectare_percentage": all_hectare_percentage,
                   "all_cent_percentage": all_cent_percentage,
                   "all_profit_sum": all_profit_sum,
                   "all_yield_area_sum": all_yield_area_sum,
                   "all_weight_percentage": all_weight_percentage}
        context = {"tree_type": tree_type,
                   "form": form, "all_sum": all_sum,
                   "data": data, "start": year_start,
                   "plants_data": plants_data,
                   "sum_tree_plan_data": sum_tree_plan_data,
                   "sum_tree_actual_data": sum_tree_actual_data,
                   "sum_tree_percentage_data": sum_tree_percentage_data,
                   "region": region,
                   "end": year_end, "tipp": tipp}
        return render(request, self.template_name, context)


class AgricultureDepartmentReport(LoginRequiredMixin, View):
    template_name = "Agriculture/reports/department.html"

    def get(self, request, pk):
        start = self.request.GET.get('start', None)
        end = self.request.GET.get('end', None)
        tipp = self.request.GET.get('type', None)
        epoch_year = date.today().year
        year_start = date(epoch_year, 1, 1)
        year_end = date(int(epoch_year) + 1, 1, 1)
        form = FilterForm(initial={"start": year_start, "end": date(epoch_year, 12, 31)})
        show_profit = False
        data = []
        if start and end:
            start = datetime.strptime(start, '%Y-%m-%d') + timedelta()
            form = FilterForm(initial={"start": start, "end": datetime.strptime(end, '%Y-%m-%d')})
            end = datetime.strptime(end, '%Y-%m-%d') + timedelta(days=1)
            epoch_year = start.year
            year_start = start
            year_end = end
        if tipp == "all":
            agriculture_plan_data = AgriculturePlan.objects.filter(date__year=epoch_year, department=pk,
                                                                   status=1).exclude(tree_type=17)
            agriculture_actual_data = AgricultureActual.objects.filter(date__range=[year_start, year_end],
                                                                       department=pk, status=1).exclude(tree_type=17)

            plant_data = TreeTypes.objects.all().exclude(id=17)
            department = Department.objects.get(id=pk)
            for plant in plant_data:
                # PLAN
                plant_hectare_plan_query = agriculture_plan_data.filter(tree_type=plant).aggregate(Sum('hectare'))
                plant_weight_plan_query = agriculture_plan_data.filter(tree_type=plant).aggregate(Sum('weight'))
                plant_hectare_plan = _check_sum_is_none(plant_hectare_plan_query['hectare__sum'])
                plant_weight_plan = _check_sum_is_none(plant_weight_plan_query['weight__sum'])
                plant_cent_plan = 0
                if plant_weight_plan and plant_hectare_plan:
                    plant_cent_plan = plant_weight_plan * 10 / plant_hectare_plan
                # AMALDA
                plant_hectare_actual_query = agriculture_actual_data.filter(tree_type=plant).aggregate(
                    Sum('hectare'))
                plant_weight_actual_query = agriculture_actual_data.filter(tree_type=plant).aggregate(Sum('weight'))

                plant_profit_actual_query = agriculture_actual_data.filter(tree_type=plant).aggregate(Sum('profit'))
                plant_yield_area_actual_query = agriculture_actual_data.filter(tree_type=plant).aggregate(
                    Sum('yield_area'))

                plant_profit_actual = _check_sum_is_none(plant_profit_actual_query['profit__sum'])
                plant_yield_area_actual = _check_sum_is_none(plant_yield_area_actual_query['yield_area__sum'])

                plant_hectare_actual = _check_sum_is_none(plant_hectare_actual_query['hectare__sum'])
                plant_weight_actual = _check_sum_is_none(plant_weight_actual_query['weight__sum'])
                plant_cent_actual = 0
                if plant_weight_actual and plant_hectare_actual:
                    plant_cent_actual = plant_weight_actual * 10 / plant_hectare_actual
                plant_hectare_percentage = _calculate_percentage(plant_hectare_plan, plant_hectare_actual)
                plant_weight_percentage = _calculate_percentage(plant_weight_plan, plant_weight_actual)
                plant_cent_percentage = _calculate_percentage(plant_cent_plan, plant_cent_actual)
                data.append({
                    "plant_name": plant.name,
                    "plant_plan_hectare": plant_hectare_plan,
                    "plant_plan_cent": plant_cent_plan,
                    "plant_plan_weight": plant_weight_plan,
                    "plant_profit_actual": plant_profit_actual,
                    "plant_yield_area_actual": plant_yield_area_actual,
                    "plant_actual_hectare": plant_hectare_actual,
                    "plant_actual_cent": plant_cent_actual,
                    "plant_actual_weight": plant_weight_actual,
                    "plant_hectare_percentage": plant_hectare_percentage,
                    "plant_cent_percentage": plant_cent_percentage,
                    "plant_weight_percentage": plant_weight_percentage

                })
            depart_profit_actual_query = agriculture_actual_data.aggregate(Sum('profit'))
            depart_yield_area_actual_query = agriculture_actual_data.aggregate(Sum('yield_area'))

            depart_profit_actual = _check_sum_is_none(depart_profit_actual_query['profit__sum'])
            depart_yield_area_actual = _check_sum_is_none(depart_yield_area_actual_query['yield_area__sum'])

            depart_hectare_plan_query = agriculture_plan_data.aggregate(Sum('hectare'))
            depart_weight_plan_query = agriculture_plan_data.aggregate(Sum('weight'))
            depart_hectare_plan = _check_sum_is_none(depart_hectare_plan_query['hectare__sum'])
            depart_weight_plan = _check_sum_is_none(depart_weight_plan_query['weight__sum'])
            depart_cent_plan = 0
            if depart_hectare_plan and depart_weight_plan:
                depart_cent_plan = depart_weight_plan * 10 / depart_hectare_plan

            depart_hectare_actual_query = agriculture_actual_data.aggregate(Sum('hectare'))
            depart_weight_actual_query = agriculture_actual_data.aggregate(Sum('weight'))
            depart_hectare_actual = _check_sum_is_none(depart_hectare_actual_query['hectare__sum'])
            depart_weight_actual = _check_sum_is_none(depart_weight_actual_query['weight__sum'])
            depart_cent_actual = 0
            if depart_hectare_actual and depart_weight_actual:
                depart_cent_actual = depart_weight_actual * 10 / depart_hectare_actual
            depart_hectare_percentage = _calculate_percentage(depart_hectare_plan, depart_hectare_actual)
            depart_cent_percentage = _calculate_percentage(depart_cent_plan, depart_cent_actual)
            depart_weight_percentage = _calculate_percentage(depart_weight_plan, depart_weight_actual)
            department = {
                "department_id": department.id,
                "depart_name": department.name,
                "depart_plan_hectare": depart_hectare_plan,
                "depart_plan_cent": depart_weight_plan,
                "depart_plan_weight": depart_cent_plan,
                "depart_actual_hectare": depart_hectare_actual,
                "depart_profit_actual": depart_profit_actual,
                "depart_yield_area_actual": depart_yield_area_actual,
                "depart_actual_cent": depart_weight_actual,
                "depart_actual_weight": depart_cent_actual,
                "depart_hectare_percentage": depart_hectare_percentage,
                "depart_cent_percentage": depart_cent_percentage,
                "depart_weight_percentage": depart_weight_percentage
            }

            context = {"data": data, "department": department, "form": form, "tipp": tipp, "show_profit": show_profit}
            return render(request, self.template_name, context)
        elif tipp != "all" and tipp:
            show_profit = TreeTypes.objects.filter(id=tipp)[0].show_profit
            agriculture_plan_data = AgriculturePlan.objects.filter(date__year=epoch_year, tree_type=tipp,
                                                                   department=pk,
                                                                   status=1)
            agriculture_actual_data = AgricultureActual.objects.filter(date__range=[year_start, year_end],
                                                                       tree_type=tipp,
                                                                       department=pk, status=1)
            plant_data = TreePlant.objects.filter(types=tipp)
            department = Department.objects.get(id=pk)
            for plant in plant_data:
                plant_hectare_plan_query = agriculture_plan_data.filter(tree_plant=plant).aggregate(Sum('hectare'))
                plant_weight_plan_query = agriculture_plan_data.filter(tree_plant=plant).aggregate(Sum('weight'))
                plant_hectare_plan = _check_sum_is_none(plant_hectare_plan_query['hectare__sum'])
                plant_weight_plan = _check_sum_is_none(plant_weight_plan_query['weight__sum'])
                plant_cent_plan = 0
                if plant_weight_plan and plant_hectare_plan:
                    plant_cent_plan = plant_weight_plan * 10 / plant_hectare_plan
                plant_hectare_actual_query = agriculture_actual_data.filter(tree_plant=plant).aggregate(
                    Sum('hectare'))
                plant_weight_actual_query = agriculture_actual_data.filter(tree_plant=plant).aggregate(
                    Sum('weight'))

                plant_profit_actual_query = agriculture_actual_data.filter(tree_plant=plant).aggregate(
                    Sum('profit'))
                plant_yield_area_actual_query = agriculture_actual_data.filter(tree_plant=plant).aggregate(
                    Sum('yield_area'))

                plant_profit_actual = _check_sum_is_none(plant_profit_actual_query['profit__sum'])
                plant_yield_area_actual = _check_sum_is_none(plant_yield_area_actual_query['yield_area__sum'])

                plant_hectare_actual = _check_sum_is_none(plant_hectare_actual_query['hectare__sum'])
                plant_weight_actual = _check_sum_is_none(plant_weight_actual_query['weight__sum'])
                plant_cent_actual = 0
                if plant_weight_actual and plant_hectare_actual:
                    plant_cent_actual = plant_weight_actual * 10 / plant_hectare_actual
                plant_hectare_percentage = _calculate_percentage(plant_hectare_plan, plant_hectare_actual)
                plant_weight_percentage = _calculate_percentage(plant_weight_plan, plant_weight_actual)
                plant_cent_percentage = _calculate_percentage(plant_cent_plan, plant_cent_actual)
                data.append({
                    "plant_name": plant.name,
                    "plant_plan_hectare": plant_hectare_plan,
                    "plant_plan_cent": plant_cent_plan,
                    "plant_plan_weight": plant_weight_plan,
                    "plant_profit_actual": plant_profit_actual,
                    "plant_yield_area_actual": plant_yield_area_actual,
                    "plant_actual_hectare": plant_hectare_actual,
                    "plant_actual_cent": plant_cent_actual,
                    "plant_actual_weight": plant_weight_actual,
                    "plant_hectare_percentage": plant_hectare_percentage,
                    "plant_cent_percentage": plant_cent_percentage,
                    "plant_weight_percentage": plant_weight_percentage

                })
            depart_hectare_plan_query = agriculture_plan_data.aggregate(Sum('hectare'))
            depart_weight_plan_query = agriculture_plan_data.aggregate(Sum('weight'))

            depart_hectare_plan = _check_sum_is_none(depart_hectare_plan_query['hectare__sum'])
            depart_weight_plan = _check_sum_is_none(depart_weight_plan_query['weight__sum'])
            depart_cent_plan = 0
            if depart_hectare_plan and depart_weight_plan:
                depart_cent_plan = depart_weight_plan * 10 / depart_hectare_plan

            depart_hectare_actual_query = agriculture_actual_data.aggregate(Sum('hectare'))
            depart_weight_actual_query = agriculture_actual_data.aggregate(Sum('weight'))
            depart_hectare_actual = _check_sum_is_none(depart_hectare_actual_query['hectare__sum'])
            depart_weight_actual = _check_sum_is_none(depart_weight_actual_query['weight__sum'])

            depart_profit_actual_query = agriculture_actual_data.aggregate(Sum('profit'))
            depart_yield_area_actual_query = agriculture_actual_data.aggregate(Sum('yield_area'))

            depart_profit_actual = _check_sum_is_none(depart_profit_actual_query['profit__sum'])
            depart_yield_area_actual = _check_sum_is_none(depart_yield_area_actual_query['yield_area__sum'])
            depart_cent_actual = 0
            if depart_hectare_actual and depart_weight_actual:
                depart_cent_actual = depart_weight_actual * 10 / depart_hectare_actual
            depart_hectare_percentage = _calculate_percentage(depart_hectare_plan, depart_hectare_actual)
            depart_cent_percentage = _calculate_percentage(depart_cent_plan, depart_cent_actual)
            depart_weight_percentage = _calculate_percentage(depart_weight_plan, depart_weight_actual)
            department = {
                "department_id": department.id,
                "depart_name": department.name,
                "depart_plan_hectare": depart_hectare_plan,
                "depart_plan_cent": depart_cent_plan,
                "depart_plan_weight": depart_weight_plan,
                "depart_actual_hectare": depart_hectare_actual,
                "depart_profit_actual": depart_profit_actual,
                "depart_yield_area_actual": depart_yield_area_actual,
                "depart_actual_cent": depart_cent_actual,
                "depart_actual_weight": depart_weight_actual,
                "depart_hectare_percentage": depart_hectare_percentage,
                "depart_cent_percentage": depart_cent_percentage,
                "depart_weight_percentage": depart_weight_percentage
            }

            context = {"data": data, "department": department, "form": form, "tipp": tipp, "show_profit": show_profit}
            return render(request, self.template_name, context)
        else:
            context = {"form": form, "show_profit": show_profit}
            return render(request, self.template_name, context)


"""Generate EXCEL reports ↓ ↓ ↓ .xlsx files"""


class AgriculturalProductXLSX(View):
    """
    http://127.0.0.1:8000/agriculture/agriculture/report/by/crops
    https://stat-urmon.uz/agriculture/only/all/report?start=2021-01-01&end=2021-12-31&type=all
    """

    def get(self, request):
        from .excel.agricultural_crops import AgriculturalCropsSheet
        from .excel.report_by_type import AgriculturalByTypeSheet
        # from .excel.report_with_profit import AgriculturalWithProfitSheet
        product_type = request.GET.get('type_id')
        start = request.GET.get('start')
        end = request.GET.get('end')
        if start and end and product_type:
            if product_type == 'all':
                xlsx = AgriculturalCropsSheet(user=self.request.user, start=start, end=end)
                return xlsx.generate_agricultural_product_excel_report()
            else:
                try:
                    obj = TreeTypes.objects.get(pk=int(product_type))
                    xlsx = AgriculturalByTypeSheet(user=self.request.user, obj=obj, start=start, end=end)
                    return xlsx.generate_agricultural_excel_by_type_report()
                    # if obj.show_profit:
                    #     xlsx = AgriculturalWithProfitSheet(obj=obj, start=start, end=end)
                    #     return xlsx.generate_agricultural_wit_profit_report()
                    # else:
                    #     xlsx = AgriculturalWithoutProfitSheet(obj=obj, start=start, end=end)
                    #     return xlsx.generate_agricultural_without_profit_report()
                except TreeTypes.DoesNotExist:
                    raise Http404("Given query not found....")
        else:
            messages.error(request, "Sana noto'g'ri kiritilgan")
            return render(request, 'Agriculture/reports/barcha_hisobot.html', {})
