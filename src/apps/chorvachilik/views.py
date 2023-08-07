import json
from datetime import timedelta, datetime, date
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.db.models import Sum
from django.shortcuts import render, redirect

from django.views import View
from django.views.generic import ListView, FormView
from django_filters.views import FilterView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ChorvachilikActualFilter, ChorvaInputOutputFilter
from .forms import *
from .serializers import UploadFileSerializer
from ..accounts.forms import FilterForm
from ..accounts.models import User, Department, Region
from ..chorvachilik.models import ChorvachilikActual, Chorvachilik, ChorvachilikPlan, ChorvachilikTypes, \
    ChorvaInputOutput, Animal, ChorvaInputOutputCategory, AnimalCategory, UploadFile
from ..finance.views import _check_sum_is_none, _calculate_percentage
from ..trees.models import TreeTypes
from ..trees.views import JsonData
from ..report.models import Report as Rp
from ..core.service import get_current_user_regions_and_departments_qs, get_current_user_regions_and_departments_json

epoch_year = date.today().year
year_start = date(epoch_year, 1, 1).strftime('%Y-%m-%d')
year_end = date(epoch_year, 12, 31).strftime('%Y-%m-%d')


class ChorvachilikActualList(LoginRequiredMixin, FilterView, ListView):
    template_name = 'chorvachilik/actual/list.html'
    model = ChorvachilikActual
    context_object_name = 'object_list'
    paginate_by = 10
    filterset_class = ChorvachilikActualFilter

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
            return ChorvachilikActual.objects.filter(region__in=regions,
                                                     department__in=departments,
                                                     status=1).order_by('-id')
        else:
            return ChorvachilikActual.objects.filter(status=44).order_by('-id')


class ChorvachilikActualCreate(LoginRequiredMixin, View):
    template_name = 'chorvachilik/actual/create.html'

    def get(self, request):
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        context = {'departments': departments,
                   'regions': regions,
                   'chorvachilik_types': JsonData().get_json_data(chorvachilik_type=True),
                   'chorvachilik': JsonData().get_json_data(chorvachilik=True)}
        return render(request, self.template_name, context)

    def post(self, request):
        data = request.POST
        items = json.loads(data['items'])

        for i in range(len(items)):
            ChorvachilikActual.objects.create(
                date=data['date'],
                department=Department.objects.get(id=data['department']),
                region=Region.objects.get(id=data['region']),
                chorvachilik_type=ChorvachilikTypes.objects.get(id=data['chorvachilik_type']),
                chorvachilik=Chorvachilik.objects.get(id=items[i]['chorvachilik']),
                amount=int(items[i]['amount']),
                amount_type=int(items[i]['amount_type']),
                creator=self.request.user
            )
        return redirect('chorvachilik:chorvachilik_actual_list')


class ChorvachilikActualDetail(LoginRequiredMixin, View):
    template_name = 'chorvachilik/actual/detail.html'

    def get(self, request, pk):
        try:
            chorvachilik = ChorvachilikActual.objects.get(pk=pk)
            form = ChorvachilikActualForm(initial={
                'date': chorvachilik.date,
                "chorvachilik": chorvachilik.chorvachilik,
                "amount": chorvachilik.amount,
                "department": chorvachilik.department,
                "creator": chorvachilik.creator,
                "region": chorvachilik.region,
                "amount_type": chorvachilik.amount_type,
                "chorvachilik_type": chorvachilik.chorvachilik_type})
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "chorvachilik": chorvachilik,
                "data": departments,
                "region": regions,
                "chorvachiliks": JsonData().get_json_data(chorvachilik=True),
                "chorvachilik_types": JsonData().get_json_data(chorvachilik_type=True),
                'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            chorvachilik = ChorvachilikActual.objects.get(pk=pk)
            form = ChorvachilikActualForm(instance=chorvachilik, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('chorvachilik:chorvachilik_actual_list')
            else:
                return redirect('chorvachilik:chorvachilik_actual_list')
        except ObjectDoesNotExist:
            return redirect('chorvachilik:chorvachilik_actual_list')


class ChorvachilikActualDeleteView(LoginRequiredMixin, View):
    template_name = 'chorvachilik/actual/list.html'

    def get(self, request, pk):
        qs = ChorvachilikActual.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('chorvachilik:chorvachilik_actual_list')
        else:
            return redirect('chorvachilik:chorvachilik_actual_list')


# Chorvachilik PLAN
class ChorvachilikPlanList(LoginRequiredMixin, ListView):
    template_name = 'chorvachilik/plan/list.html'
    paginate_by = 10
    model = ChorvachilikPlan

    def get_context_data(self, *args, **kwargs):
        context = super(ChorvachilikPlanList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return ChorvachilikPlan.objects.filter(region__in=regions, department__in=departments, status=1).order_by(
                '-id')
        else:
            return ChorvachilikPlan.objects.filter(status=44).order_by('-id')


class ChorvachilikPlanCreate(LoginRequiredMixin, View):
    template_name = 'chorvachilik/plan/create.html'

    def get(self, request):
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        context = {'departments': departments,
                   'regions': regions,
                   'chorvachilik_types': JsonData().get_json_data(chorvachilik_type=True),
                   'chorvachilik': JsonData().get_json_data(chorvachilik=True)}
        return render(request, self.template_name, context)

    def post(self, request):
        data = request.POST
        next_button = json.loads(data['next'])
        ChorvachilikPlan.objects.create(
            date=data['date'],
            department=Department.objects.get(id=data['department']),
            region=Region.objects.get(id=data['region']),
            chorvachilik_type=ChorvachilikTypes.objects.get(id=data['chorvachilik_type']),
            chorvachilik=Chorvachilik.objects.get(id=data['chorvachilik']),
            amount=int(data['amount']),
            amount_type=int(data['amount_type']),
            creator=self.request.user
        )
        if next_button:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            ctx = {"departments": departments,
                   "regions": regions,
                   "chorvachilik_types": JsonData().get_json_data(chorvachilik_type=True),
                   "chorvachiliks": JsonData().get_json_data(chorvachilik=True)}
            return render(request, self.template_name, ctx)
        else:
            return redirect('chorvachilik:chorvachilik_plan_list')


class ChorvachilikPlanDeleteView(LoginRequiredMixin, View):
    template_name = 'chorvachilik/plan/list.html'

    def get(self, request, pk):
        qs = ChorvachilikPlan.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('chorvachilik:chorvachilik_plan_list')
        else:
            return redirect('chorvachilik:chorvachilik_plan_list')


class ChorvachilikPlanDetail(LoginRequiredMixin, View):
    template_name = 'chorvachilik/plan/detail.html'

    def get(self, request, pk):
        try:
            chorvachilik = ChorvachilikPlan.objects.get(pk=pk)
            form = ChorvachilikActualForm(initial={
                'date': chorvachilik.date,
                "chorvachilik": chorvachilik.chorvachilik,
                "amount": chorvachilik.amount,
                "department": chorvachilik.department,
                "creator": chorvachilik.creator,
                "region": chorvachilik.region,
                "amount_type": chorvachilik.amount_type,
                "chorvachilik_type": chorvachilik.chorvachilik_type})
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "chorvachilik": chorvachilik,
                "data": departments,
                "region": regions,
                "chorvachiliks": JsonData().get_json_data(chorvachilik=True),
                "chorvachilik_types": JsonData().get_json_data(chorvachilik_type=True),
                'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            chorvachilik = ChorvachilikPlan.objects.get(pk=pk)
            form = ChorvachilikActualForm(instance=chorvachilik, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('chorvachilik:chorvachilik_plan_list')
            else:
                return redirect('chorvachilik:chorvachilik_plan_list')
        except ObjectDoesNotExist:
            return redirect('chorvachilik:chorvachilik_plan_list')


# CHORVACHILIK REPORT
class ChorvachilikReportDashboardView(LoginRequiredMixin, View):
    template_name = "chorvachilik/reports/dashboard.html"

    def get(self, request):
        data = Rp.objects.filter(type=3, status=1)
        type_name = ChorvachilikTypes.objects.filter(status=1).first().name

        ctx = {"start": year_start, "end": year_end,
               "type": type_name, "data": data, "current_year": date.today().year}
        return render(request, self.template_name, ctx)


class ChorvachilikAllReportsView(LoginRequiredMixin, View):
    template_name = "chorvachilik/reports/regions_and_departments.html"

    def get(self, request):
        tipp = self.request.GET.get('type', None)
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
        region_obj = None
        region_id = None
        all_amount_plan_sum = 0
        all_amount_actual_sum = 0
        data = []
        if not tipp:
            tipp = ChorvachilikTypes.objects.filter(status=1).first().name
        type_id = ChorvachilikTypes.objects.filter(name=tipp).first().id
        form = ChorvachilikFilterForm(initial={"start": year_start, "end": year_end, "type": tipp})
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            animal_actual_data = ChorvachilikActual.objects.filter(date__year=current_year, chorvachilik_type__name=tipp,
                                                                   status=1)
            animal_plan_data = ChorvachilikPlan.objects.filter(date__range=[year_start, year_end],
                                                               chorvachilik_type__name=tipp, status=1)
            x = 1
            for department in departments:
                x = x + 1
                # PLAN
                depart_plan_amount_query = animal_plan_data.filter(department=department).aggregate(Sum('amount'))
                depart_plan_amount = _check_sum_is_none(depart_plan_amount_query['amount__sum'])
                # amalda
                depart_actual_amount_query = animal_actual_data.filter(department=department).aggregate(Sum('amount'))
                depart_actual_amount = _check_sum_is_none(depart_actual_amount_query['amount__sum'])
                depart_amount_percentage = _calculate_percentage(depart_plan_amount, depart_actual_amount)

                if region_id != department.region_id:
                    region_obj = Region.objects.get(id=department.region_id)
                    # PLAN
                    region_plan_amount_query = animal_plan_data.filter(region=region_obj).aggregate(Sum('amount'))
                    region_plan_amount = _check_sum_is_none(region_plan_amount_query['amount__sum'])
                    # AMALDA
                    region_actual_amount_query = animal_actual_data.filter(region=region_obj).aggregate(Sum('amount'))
                    region_actual_amount = _check_sum_is_none(region_actual_amount_query['amount__sum'])
                    # PERCENTAGE
                    region_amount_percentage = _calculate_percentage(region_plan_amount, region_actual_amount)

                    all_amount_plan_sum += region_plan_amount
                    all_amount_actual_sum += region_actual_amount

                    data.append({
                        "index": 1,
                        "region_id": region_obj.id,
                        "region_name": region_obj.name,
                        "region_amount_plan": region_plan_amount,
                        "region_amount_actual": region_actual_amount,
                        "region_amount_percentage": region_amount_percentage,

                        "department_id": department.id,
                        "department_name": department.name,
                        "department_amount_plan": depart_plan_amount,
                        "department_amount_actual": depart_actual_amount,
                        "department_amount_percentage": depart_amount_percentage,
                    })
                    x = 1
                else:
                    data.append({
                        "index": x,
                        "department_id": department.id,
                        "department_name": department.name,
                        "department_amount_plan": depart_plan_amount,
                        "department_amount_actual": depart_actual_amount,
                        "department_amount_percentage": depart_amount_percentage,
                    })
                region_obj = None
                region_id = department.region_id
            all_amount_percentage = _calculate_percentage(all_amount_plan_sum, all_amount_actual_sum)
            all_sum = {"all_amount_plan_sum": all_amount_plan_sum, "all_amount_actual_sum": all_amount_actual_sum,
                       "all_amount_percentage": all_amount_percentage}
            context = {"chorvachilik_types": JsonData().get_json_data(chorvachilik_type=True),
                       "form": form, "all_sum": all_sum,
                       "data": data, "start": year_start,
                       "end": year_end, "tipp": tipp,
                       "current_year":current_year,
                       "type_id": type_id}
        else:
            context = {"chorvachilik_types": JsonData().get_json_data(chorvachilik_type=True),
                       "form": form, "start": year_start,
                       "end": year_end, "tipp": tipp,
                       "current_year":current_year,
                       "type_id": type_id}
        return render(request, self.template_name, context)


class ChorvachilikRegionReport(LoginRequiredMixin, View):
    template_name = "chorvachilik/reports/region.html"

    def get(self, request, pk):
        start = self.request.GET.get('start', None)
        end = self.request.GET.get('end', None)
        tipp = self.request.GET.get('type', None)
        epoch_year = date.today().year
        year_start = date(epoch_year, 1, 1)
        year_end = date(epoch_year, 12, 31)
        data = []
        if not tipp:
            tipp = ChorvachilikTypes.objects.filter(status=1).first().name
        form = ChorvachilikFilterForm(initial={"start": year_start, "end": year_end, "type": tipp})
        if start and end:
            start = datetime.strptime(start, '%Y-%m-%d') + timedelta()
            form = ChorvachilikFilterForm(
                initial={"start": start, "end": datetime.strptime(end, '%Y-%m-%d'), "type": tipp})
            end = datetime.strptime(end, '%Y-%m-%d') + timedelta(days=1)
            epoch_year = start.year
            year_start = start
            year_end = end
        chorvachilik_plan_data = ChorvachilikPlan.objects.filter(date__year=epoch_year,
                                                                 chorvachilik_type__name=tipp,
                                                                 region=pk, status=1)
        chorvachilik_actual_data = ChorvachilikActual.objects.filter(date__range=[year_start, year_end],
                                                                     chorvachilik_type__name=tipp, region=pk,
                                                                     status=1)
        chorvachilik_data = Chorvachilik.objects.filter(type__name=tipp)
        region = Region.objects.get(id=pk)
        for chorvachilik in chorvachilik_data:
            # PLAN
            chorvachilik_amount_plan_query = chorvachilik_plan_data.filter(chorvachilik=chorvachilik).aggregate(
                Sum('amount'))
            chorvachilik_amount_plan = _check_sum_is_none(chorvachilik_amount_plan_query['amount__sum'])
            # ACTUAL
            chorvachilik_amount_actual_query = chorvachilik_actual_data.filter(chorvachilik=chorvachilik).aggregate(
                Sum('amount'))
            chorvachilik_amount_actual = _check_sum_is_none(chorvachilik_amount_actual_query['amount__sum'])

            chorvachilik_percentage = _calculate_percentage(chorvachilik_amount_plan, chorvachilik_amount_actual)
            data.append({
                "chorva_name": chorvachilik.name,
                "chorva_amount_plan": chorvachilik_amount_plan,
                "chorva_amount_actual": chorvachilik_amount_actual,
                "chorva_percentage": chorvachilik_percentage

            })
        region_amount_plan_query = chorvachilik_plan_data.aggregate(Sum('amount'))
        region_amount_actual_query = chorvachilik_actual_data.aggregate(Sum('amount'))
        region_amount_plan = _check_sum_is_none(region_amount_plan_query['amount__sum'])
        region_amount_actual = _check_sum_is_none(region_amount_actual_query['amount__sum'])
        region_percentage = _calculate_percentage(region_amount_plan, region_amount_actual)
        region = {
            "region_id": region.id,
            "region_name": region.name,
            "region_amount_plan": region_amount_plan,
            "region_amount_actual": region_amount_actual,
            "region_percentage": region_percentage
        }
        context = {"data": data, "region": region,
                   "form": form, "tipp": tipp,
                   "chorvachilik_types": JsonData().get_json_data(chorvachilik_type=True)}
        return render(request, self.template_name, context)


class ChorvachilikDepartmentReport(LoginRequiredMixin, View):
    template_name = "chorvachilik/reports/department.html"

    def get(self, request, pk):
        start = self.request.GET.get('start', None)
        end = self.request.GET.get('end', None)
        tipp = self.request.GET.get('type', None)
        epoch_year = date.today().year
        year_start = date(epoch_year, 1, 1)
        year_end = date(epoch_year, 12, 31)
        data = []
        if not tipp:
            tipp = ChorvachilikTypes.objects.filter(status=1).first().id
        form = ChorvachilikFilterForm(initial={"start": year_start, "end": year_end, "type": tipp})
        if start and end:
            start = datetime.strptime(start, '%Y-%m-%d') + timedelta()
            form = ChorvachilikFilterForm(
                initial={"start": start, "end": datetime.strptime(end, '%Y-%m-%d'), "type": tipp})
            end = datetime.strptime(end, '%Y-%m-%d') + timedelta(days=1)
            epoch_year = start.year
            year_start = start
            year_end = end
        chorvachilik_plan_data = ChorvachilikPlan.objects.filter(date__year=epoch_year,
                                                                 chorvachilik_type__name=tipp,
                                                                 department=pk, status=1)
        chorvachilik_actual_data = ChorvachilikActual.objects.filter(date__range=[year_start, year_end],
                                                                     chorvachilik_type__name=tipp, department=pk,
                                                                     status=1)
        chorvachilik_data = Chorvachilik.objects.filter(type__name=tipp)
        department = Department.objects.get(id=pk)
        for chorvachilik in chorvachilik_data:
            # PLAN
            chorvachilik_amount_plan_query = chorvachilik_plan_data.filter(chorvachilik=chorvachilik).aggregate(
                Sum('amount'))
            chorvachilik_amount_plan = _check_sum_is_none(chorvachilik_amount_plan_query['amount__sum'])
            # ACTUAL
            chorvachilik_amount_actual_query = chorvachilik_actual_data.filter(chorvachilik=chorvachilik).aggregate(
                Sum('amount'))
            chorvachilik_amount_actual = _check_sum_is_none(chorvachilik_amount_actual_query['amount__sum'])

            chorvachilik_percentage = _calculate_percentage(chorvachilik_amount_plan, chorvachilik_amount_actual)
            data.append({
                "chorva_name": chorvachilik.name,
                "chorva_amount_plan": chorvachilik_amount_plan,
                "chorva_amount_actual": chorvachilik_amount_actual,
                "chorva_percentage": chorvachilik_percentage
            })
        depart_amount_plan_query = chorvachilik_plan_data.aggregate(Sum('amount'))
        depart_amount_actual_query = chorvachilik_actual_data.aggregate(Sum('amount'))
        depart_amount_plan = _check_sum_is_none(depart_amount_plan_query['amount__sum'])
        depart_amount_actual = _check_sum_is_none(depart_amount_actual_query['amount__sum'])
        depart_percentage = _calculate_percentage(depart_amount_plan, depart_amount_actual)
        department = {
            "department_id": department.id,
            "depart_name": department.name,
            "depart_amount_plan": depart_amount_plan,
            "depart_amount_actual": depart_amount_actual,
            "depart_percentage": depart_percentage
        }
        context = {"data": data, "department": department,
                   "form": form, "tipp": tipp,
                   "chorvachilik_types": JsonData().get_json_data(chorvachilik_type=True)}
        return render(request, self.template_name, context)


class ChorvaInputList(LoginRequiredMixin, FilterView, ListView):
    template_name = 'chorvachilik/input/list.html'
    model = ChorvachilikActual
    context_object_name = 'object_list'
    paginate_by = 10
    filterset_class = ChorvaInputOutputFilter

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
            return ChorvaInputOutput.objects.filter(region__in=regions,
                                                    department__in=departments,
                                                    type=1, status=1).order_by('-id')
        else:
            return ChorvaInputOutput.objects.filter(type=1, status=44).order_by('-id')


class ChorvaInputCreate(LoginRequiredMixin, View):
    template_name = 'chorvachilik/input/create.html'

    def get(self, request):
        form = InputOutputForm()
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        ctx = {"departments": departments,
               "regions": regions,
               "animal": JsonData().get_json_data(animal=True),
               "category": serialize("json", ChorvaInputOutputCategory.objects.filter(status=1, type=1)),
               "animal_category": serialize("json", AnimalCategory.objects.filter(status=1)),
               "form": form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        # items = json.loads(data['items'])
        nextt = json.loads(data['next'])
        ChorvaInputOutput.objects.create(
            date=data['date'],
            department=Department.objects.get(id=data['department']),
            region=Region.objects.get(id=data['region']),
            category=ChorvaInputOutputCategory.objects.get(id=data['category']),
            animal=Animal.objects.get(id=data['animal']),
            amount=float(data['amount']),
            weight=float(data['weight']),
            type=float(data['type']),
            creator=self.request.user
        )
        if nextt:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            ctx = {"departments": departments,
                   "regions": regions,
                   "animal": JsonData().get_json_data(animal=True),
                   "category": JsonData().get_json_data(in_out_category=True),
                   "animal_category": serialize("json", AnimalCategory.objects.filter(status=1))}
            return render(request, self.template_name, ctx)
        else:
            return redirect('chorvachilik:chorva_input_list')


class ChorvaInputDetail(LoginRequiredMixin, View):
    template_name = 'chorvachilik/input/detail.html'

    def get(self, request, pk):
        try:
            input = ChorvaInputOutput.objects.get(pk=pk)
            form = InputOutputForm(initial={
                'date': input.date,
                "department": input.department,
                "region": input.region,
                "category": input.category,
                "animal": input.animal,
                "amount": input.amount,
                "weight": input.weight,
                "type": input.type})
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "chorvainput": input,
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
            chorva_input = ChorvaInputOutput.objects.get(pk=pk)
            form = InputOutputForm(instance=chorva_input, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('chorvachilik:chorva_input_list')
            else:
                return redirect('chorvachilik:chorva_input_list')
        except ObjectDoesNotExist:
            return redirect('chorvachilik:chorva_input_list')


class ChorvaInputDeleteView(LoginRequiredMixin, View):
    template_name = 'chorvachilik/input/list.html'
    permission_required = 'chorvachilik.delete_chorvainputoutput'

    def get(self, request, pk):
        qs = ChorvaInputOutput.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=3)
            return redirect('chorvachilik:chorva_input_list')
        else:
            return redirect('chorvachilik:chorva_input_list')


# CHORVA OUTPUT
class ChorvaOutputList(LoginRequiredMixin, FilterView, ListView):
    template_name = 'chorvachilik/output/list.html'
    model = ChorvachilikActual
    context_object_name = 'object_list'
    paginate_by = 10
    filterset_class = ChorvaInputOutputFilter

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
            return ChorvaInputOutput.objects.filter(region__in=regions, department__in=departments, type=2,
                                                    status=1).order_by('-id')
        else:
            return ChorvaInputOutput.objects.filter(type=2, status=44).order_by('-id')


class ChorvaOutputCreate(LoginRequiredMixin, View):
    template_name = 'chorvachilik/output/create.html'

    def get(self, request):
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        ctx = {"departments": departments,
               "regions": regions,
               "animal": JsonData().get_json_data(animal=True),
               "category": serialize("json", ChorvaInputOutputCategory.objects.filter(status=1, type=2)),
               "animal_category": serialize("json", AnimalCategory.objects.filter(status=1)),
               }
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        nextt = json.loads(data['next'])
        if data:
            images = json.loads(data['images'])
            current = ChorvaInputOutput.objects.create(
                date=data['date'],
                department=Department.objects.get(id=data['department']),
                region=Region.objects.get(id=data['region']),
                category=ChorvaInputOutputCategory.objects.get(id=data['category']),
                animal=Animal.objects.get(id=data['animal']),
                amount=data['amount'],
                weight=data['weight'],
                type=2,
                creator=self.request.user
            )
            if images and current:
                for item in images:
                    UploadFile.objects.filter(id=item).update(output=current)
            if nextt:
                regions, departments = get_current_user_regions_and_departments_json(self.request.user)
                ctx = {"departments": departments,
                       "regions": regions,
                       "animal": JsonData().get_json_data(animal=True),
                       "category": serialize("json", ChorvaInputOutputCategory.objects.filter(status=1, type=2)),
                       "animal_category": serialize("json", AnimalCategory.objects.filter(status=1)),
                       "state": True}
                return render(request, self.template_name, ctx)
            else:
                return redirect('chorvachilik:chorva_output_list')
        else:
            ctx = {'state': False}
            return redirect('chorvachilik:chorva_output_create', ctx)


class ChorvaOutputDetail(LoginRequiredMixin, View):
    template_name = 'chorvachilik/output/detail.html'

    def get(self, request, pk):
        try:
            output = ChorvaInputOutput.objects.get(pk=pk)
            form = InputOutputForm(initial={
                'date': output.date,
                "department": output.department,
                "region": output.region,
                "category": output.category,
                "animal": output.animal,
                "amount": output.amount,
                "weight": output.weight})
            images = serialize('json', UploadFile.objects.filter(output=output))
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "chorvainput": output,
                "data": departments,
                "region": regions,
                'form': form,
                "images": images,
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            chorva_input = ChorvaInputOutput.objects.get(pk=pk)
            form = InputOutputForm(instance=chorva_input, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('chorvachilik:chorva_output_list')
            else:
                return redirect('chorvachilik:chorva_output_list')
        except ObjectDoesNotExist:
            return redirect('chorvachilik:chorva_output_list')


class ChorvaOutputDeleteView(LoginRequiredMixin, View):
    template_name = 'chorvachilik/output/list.html'

    def get(self, request, pk):
        qs = ChorvaInputOutput.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=3)
            return redirect('chorvachilik:chorva_output_list')
        else:
            return redirect('chorvachilik:chorva_output_list')


# CHORVA INPUT OUTPUT REPORT
class ChorvaInOutDashboard(LoginRequiredMixin, View):
    template_name = "chorvachilik/in_out_report/dashboard.html"

    def get(self, request):
        animal_category = AnimalCategory.objects.filter(status=1).first().name
        ctx = {"start": year_start, "end": year_end, "animal_category": animal_category}
        return render(request, self.template_name, ctx)


class ChorvaInOutAllReport(LoginRequiredMixin, View):
    template_name = "chorvachilik/in_out_report/regions_and_departments.html"

    def get(self, request):
        category = self.request.GET.get('category', None)
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

        region_obj = None
        region_id = None
        data = []
        if not category:
            category = AnimalCategory.objects.filter(status=1).first().name
        form = ChorvaInOutFilterForm(initial={"start": year_start, "end": year_end, "category": category})
        chorva_in_out_data = ChorvaInputOutput.objects.filter(status=1, animal__category__name=category,
                                                              date__range=[year_start, year_end])

        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            x = 1
            for depart in departments:
                x = x + 1
                depart_in_amount_query = chorva_in_out_data.filter(type=1, department=depart).aggregate(Sum('amount'))
                depart_in_weight_query = chorva_in_out_data.filter(type=1, department=depart).aggregate(Sum('weight'))

                depart_out_amount_query = chorva_in_out_data.filter(type=2, department=depart).aggregate(Sum('amount'))
                depart_out_weight_query = chorva_in_out_data.filter(type=2, department=depart).aggregate(Sum('weight'))

                depart_in_amount = _check_sum_is_none(depart_in_amount_query['amount__sum'])
                depart_in_weight = _check_sum_is_none(depart_in_weight_query['weight__sum'])

                depart_out_amount = _check_sum_is_none(depart_out_amount_query['amount__sum'])
                depart_out_weight = _check_sum_is_none(depart_out_weight_query['weight__sum'])
                if region_id != depart.region_id:
                    region_obj = Region.objects.get(id=depart.region_id)
                    region_in_amount_query = chorva_in_out_data.filter(type=1, region=region_obj).aggregate(
                        Sum('amount'))
                    region_in_weight_query = chorva_in_out_data.filter(type=1, region=region_obj).aggregate(
                        Sum('weight'))

                    region_out_amount_query = chorva_in_out_data.filter(type=2, region=region_obj).aggregate(
                        Sum('amount'))
                    region_out_weight_query = chorva_in_out_data.filter(type=2, region=region_obj).aggregate(
                        Sum('weight'))

                    region_in_amount = _check_sum_is_none(region_in_amount_query['amount__sum'])
                    region_in_weight = _check_sum_is_none(region_in_weight_query['weight__sum'])

                    region_out_amount = _check_sum_is_none(region_out_amount_query['amount__sum'])
                    region_out_weight = _check_sum_is_none(region_out_weight_query['weight__sum'])
                    data.append({
                        "index": 1,
                        "region_id": region_obj.id,
                        "region_name": region_obj.name,
                        "region_in_amount": region_in_amount,
                        "region_in_weight": region_in_weight,
                        "region_out_amount": region_out_amount,
                        "region_out_weight": region_out_weight,

                        "depart_id": depart.id,
                        "depart_name": depart.name,
                        "depart_in_amount": depart_in_amount,
                        "depart_in_weight": depart_in_weight,
                        "depart_out_amount": depart_out_amount,
                        "depart_out_weight": depart_out_weight
                    })
                    x = 1
                else:
                    data.append({
                        "index": x,
                        "depart_id": depart.id,
                        "depart_name": depart.name,
                        "depart_in_amount": depart_in_amount,
                        "depart_in_weight": depart_in_weight,
                        "depart_out_amount": depart_out_amount,
                        "depart_out_weight": depart_out_weight,

                    })
                region_obj = None
                region_id = depart.region_id
            all_in_amount_query = chorva_in_out_data.filter(type=1).aggregate(Sum('amount'))
            all_in_weight_query = chorva_in_out_data.filter(type=1).aggregate(Sum('weight'))
            all_out_amount_query = chorva_in_out_data.filter(type=2).aggregate(Sum('amount'))
            all_out_weight_query = chorva_in_out_data.filter(type=2).aggregate(Sum('weight'))
            all_in_amount = _check_sum_is_none(all_in_amount_query['amount__sum'])
            all_in_weight = _check_sum_is_none(all_in_weight_query['weight__sum'])
            all_out_amount = _check_sum_is_none(all_out_amount_query['amount__sum'])
            all_out_weight = _check_sum_is_none(all_out_weight_query['weight__sum'])
            all_sum = {
                "all_in_amount__sum": all_in_amount,
                "all_in_weight__sum": all_in_weight,
                "all_out_amount__sum": all_out_amount,
                "all_out_weight__sum": all_out_weight
            }
            ctx = {"data": data,
                   "form": form,
                   "all_sum": all_sum,
                   "start": year_start,
                   "category": category,
                   "end": year_end}
            return render(request, self.template_name, ctx)
        else:
            ctx = {"form": form,
                   "start": year_start,
                   "category": category,
                   "end": year_end}
            return render(request, self.template_name, ctx)


class ChorvaInOutDeparmentReport(LoginRequiredMixin, View):
    template_name = "chorvachilik/in_out_report/department.html"

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
        data = []
        # if not category:
        #     category = AnimalCategory.objects.filter(status=1).first().name
        form = FilterForm(initial={"start": year_start, "end": year_end})
        department = Department.objects.get(id=pk)
        chorva_in_out_data = ChorvaInputOutput.objects.filter(status=1, department=department,
                                                              date__range=[year_start, year_end])
        # animals_data = Animal.objects.filter(category__name=category, status=1)
        animals_data = Animal.objects.filter(status=1)
        for animal in animals_data:
            animal_in_amount_query = chorva_in_out_data.filter(type=1, animal=animal).aggregate(Sum('amount'))
            animal_in_weight_query = chorva_in_out_data.filter(type=1, animal=animal).aggregate(Sum('weight'))

            animal_out_amount_query = chorva_in_out_data.filter(type=2, animal=animal).aggregate(Sum('amount'))
            animal_out_weight_query = chorva_in_out_data.filter(type=2, animal=animal).aggregate(Sum('weight'))

            animal_in_amount = _check_sum_is_none(animal_in_amount_query['amount__sum'])
            animal_in_weight = _check_sum_is_none(animal_in_weight_query['weight__sum'])

            animal_out_amount = _check_sum_is_none(animal_out_amount_query['amount__sum'])
            animal_out_weight = _check_sum_is_none(animal_out_weight_query['weight__sum'])

            data.append({
                "animal_id": animal.id,
                "animal_name": animal.name,
                "animal_in_amount": animal_in_amount,
                "animal_in_weight": animal_in_weight,
                "animal_out_amount": animal_out_amount,
                "animal_out_weight": animal_out_weight
            })
        all_in_amount_query = chorva_in_out_data.filter(type=1).aggregate(Sum('amount'))
        all_in_weight_query = chorva_in_out_data.filter(type=1).aggregate(Sum('weight'))
        all_out_amount_query = chorva_in_out_data.filter(type=2).aggregate(Sum('amount'))
        all_out_weight_query = chorva_in_out_data.filter(type=2).aggregate(Sum('weight'))
        all_in_amount = _check_sum_is_none(all_in_amount_query['amount__sum'])
        all_in_weight = _check_sum_is_none(all_in_weight_query['weight__sum'])
        all_out_amount = _check_sum_is_none(all_out_amount_query['amount__sum'])
        all_out_weight = _check_sum_is_none(all_out_weight_query['weight__sum'])
        all_sum = {
            "department": department,
            "all_in_amount__sum": all_in_amount,
            "all_in_weight__sum": all_in_weight,
            "all_out_amount__sum": all_out_amount,
            "all_out_weight__sum": all_out_weight
        }
        ctx = {"data": data,
               "form": form,
               "all_sum": all_sum,
               "start": year_start,
               "end": year_end,
               "current_year":current_year}
        return render(request, self.template_name, ctx)


# ANIMAL CRUD
class AnimalList(LoginRequiredMixin, View):
    template_name = 'chorvachilik/animal/list.html'
    paginate_by = 4

    def get(self, request):
        try:
            animals = Animal.objects.exclude(status=2).order_by('-id')
            context = {
                "is_user": True, "animals": animals
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)


class AnimalDetail(LoginRequiredMixin, View):
    template_name = 'chorvachilik/animal/detail.html'

    def get(self, request, pk):
        try:
            animal = Animal.objects.get(pk=pk)
            form = AnimalForm(initial={'name': animal.name})
            context = {
                "is_user": True, "animal": animal, 'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            animal = Animal.objects.get(pk=pk)
            form = AnimalForm(instance=animal, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('chorvachilik:animal_list')
            else:
                return redirect('chorvachilik:animal_list')
        except ObjectDoesNotExist:
            return redirect('chorvachilik:animal_list')


class AnimalCreate(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/register"""
    template_name = 'chorvachilik/animal/create.html'

    def get(self, request):
        try:
            form = AnimalForm()
            context = {
                "is_user": True, "form": form,
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request):
        try:
            form = AnimalForm(data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Account updated successfully!")
                return redirect('chorvachilik:animal_list')
            else:
                messages.error(request, 'Something went wrong')
                return redirect('chorvachilik:animal_list')
        except ObjectDoesNotExist:
            return redirect('chorvachilik:animal_list')


class AnimalDeleteView(LoginRequiredMixin, View):
    template_name = 'chorvachilik/animal/list.html'

    def get(self, request, pk):
        qs = Animal.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('chorvachilik:animal_list')
        else:
            return redirect('chorvachilik:animal_list')


# ANIMAL CATEGORY CREATE
class AnimalCategoryList(LoginRequiredMixin, View):
    template_name = 'chorvachilik/animal_category/list.html'
    paginate_by = 4

    def get(self, request):
        try:
            animals = AnimalCategory.objects.filter(status=1).order_by('-id')
            context = {
                "is_user": True, "items": animals
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)


class AnimalCategoryDetail(LoginRequiredMixin, View):
    template_name = 'chorvachilik/animal_category/detail.html'

    def get(self, request, pk):
        try:
            category = AnimalCategory.objects.get(pk=pk)
            form = AnimalCategoryForm(initial={'name': category.name})
            context = {
                "is_user": True, "category": category, 'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            category = AnimalCategory.objects.get(pk=pk)
            form = AnimalCategoryForm(instance=category, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('chorvachilik:animal_category_list')
            else:
                return redirect('chorvachilik:animal_category_list')
        except ObjectDoesNotExist:
            return redirect('chorvachilik:animal_category_list')


class AnimalCategoryCreate(LoginRequiredMixin, View):
    template_name = 'chorvachilik/animal_category/create.html'

    def get(self, request):
        try:
            form = AnimalCategoryForm()
            context = {
                "is_user": True, "form": form,
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request):
        try:
            form = AnimalCategoryForm(data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Account updated successfully!")
                return redirect('chorvachilik:animal_category_list')
            else:
                messages.error(request, 'Something animal_category_list wrong')
                return redirect('chorvachilik:animal_category_list')
        except ObjectDoesNotExist:
            return redirect('chorvachilik:animal_category_list')


class AnimalCategoryDeleteView(LoginRequiredMixin, View):
    template_name = 'chorvachilik/animal_category/list.html'

    def get(self, request, pk):
        qs = AnimalCategory.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('chorvachilik:animal_category_list')
        else:
            return redirect('chorvachilik:animal_category_list')


# INPUT OUTPUT CATEGORIES CRUD
class IoCategoryList(LoginRequiredMixin, View):
    template_name = 'chorvachilik/input_output_category/list.html'
    paginate_by = 4

    def get(self, request):
        try:
            data = ChorvaInputOutputCategory.objects.filter(status=1).order_by('-id')
            context = {
                "is_user": True, "items": data
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)


class IoCategoryDetail(LoginRequiredMixin, View):
    template_name = 'chorvachilik/input_output_category/detail.html'

    def get(self, request, pk):
        try:
            category = ChorvaInputOutputCategory.objects.get(pk=pk)
            form = OutputCategoryForm(initial={'name': category.name})
            context = {
                "is_user": True, "category": category, 'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            category = ChorvaInputOutputCategory.objects.get(pk=pk)
            form = OutputCategoryForm(instance=category, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('chorvachilik:in_out_category_list')
            else:
                return redirect('chorvachilik:in_out_category_list')
        except ObjectDoesNotExist:
            return redirect('chorvachilik:in_out_category_list')


class IoCategoryCreate(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/register"""
    template_name = 'chorvachilik/input_output_category/create.html'

    def get(self, request):
        try:
            form = OutputCategoryForm()
            context = {
                "is_user": True, "form": form,
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request):
        try:
            form = OutputCategoryForm(data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Account updated successfully!")
                return redirect('chorvachilik:in_out_category_list')
            else:
                messages.error(request, 'Something went wrong')
                return redirect('chorvachilik:in_out_category_list')
        except ObjectDoesNotExist:
            return redirect('chorvachilik:in_out_category_list')


class IoCategoryDeleteView(LoginRequiredMixin, View):
    template_name = 'chorvachilik/input_output_category/list.html'

    def get(self, request, pk):
        qs = ChorvaInputOutputCategory.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('chorvachilik:in_out_category_list')
        else:
            return redirect('chorvachilik:in_out_category_list')


# INPUT OUTPUT CATEGORIES CRUD
class ChorvaTypeList(LoginRequiredMixin, View):
    template_name = 'chorvachilik/chorva_type/list.html'
    paginate_by = 4

    def get(self, request):
        try:
            data = ChorvachilikTypes.objects.exclude(status=2).order_by('-id')
            context = {"is_user": True, "items": data}
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)


class ChorvaTypeDetail(LoginRequiredMixin, View):
    template_name = 'chorvachilik/chorva_type/detail.html'

    def get(self, request, pk):
        try:
            chorva_type = ChorvachilikTypes.objects.get(pk=pk)
            form = ChorvachilikTypesForm(initial={'name': chorva_type.name})
            context = {
                "is_user": True, "type": chorva_type, 'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            chorva_type = ChorvachilikTypes.objects.get(pk=pk)
            form = ChorvachilikTypesForm(instance=chorva_type, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('chorvachilik:chorva_type_list')
            else:
                return redirect('chorvachilik:chorva_type_list')
        except ObjectDoesNotExist:
            return redirect('chorvachilik:chorva_type_list')


class ChorvaTypeCreate(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/register"""
    template_name = 'chorvachilik/chorva_type/create.html'

    def get(self, request):
        try:
            form = ChorvachilikTypesForm()
            context = {
                "is_user": True, "form": form,
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request):
        try:
            form = ChorvachilikTypesForm(data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Account updated successfully!")
                return redirect('chorvachilik:chorva_type_list')
            else:
                messages.error(request, 'Something went wrong')
                return redirect('chorvachilik:chorva_type_list')
        except ObjectDoesNotExist:
            return redirect('chorvachilik:chorva_type_list')


class ChorvaTypeDeleteView(LoginRequiredMixin, View):
    template_name = 'chorvachilik/chorva_type/list.html'

    def get(self, request, pk):
        qs = ChorvachilikTypes.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('chorvachilik:chorva_type_list')
        else:
            return redirect('chorvachilik:chorva_type_list')


# CHORVACHILIK
class ChorvaCategoryList(LoginRequiredMixin, View):
    template_name = 'chorvachilik/chorva_category/list.html'
    paginate_by = 4

    def get(self, request):
        try:
            data = Chorvachilik.objects.filter(status=1).order_by('-id')
            context = {
                "is_user": True, "items": data
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)


class ChorvaCategoryCreate(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/register"""
    template_name = 'chorvachilik/chorva_category/create.html'

    def get(self, request):
        try:
            form = ChorvachilikForm()
            context = {
                "is_user": True, "form": form,
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request):
        try:
            form = ChorvachilikForm(data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Account updated successfully!")
                return redirect('chorvachilik:chorva_category_list')
            else:
                messages.error(request, 'Something went wrong')
                return redirect('chorvachilik:chorva_category_list')
        except ObjectDoesNotExist:
            return redirect('chorvachilik:chorva_category_list')


class ChorvaCategoryDetail(LoginRequiredMixin, View):
    template_name = 'chorvachilik/chorva_category/detail.html'

    def get(self, request, pk):
        try:
            category = Chorvachilik.objects.get(pk=pk)
            form = ChorvachilikForm(initial={'name': category.name, "type": category.type.all()})
            context = {
                "is_user": True, "category": category, 'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            category = Chorvachilik.objects.get(pk=pk)
            form = ChorvachilikForm(instance=category, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('chorvachilik:chorva_category_list')
            else:
                return redirect('chorvachilik:chorva_category_list')
        except ObjectDoesNotExist:
            return redirect('chorvachilik:chorva_category_list')


class ChorvaCategoryDeleteView(LoginRequiredMixin, View):
    template_name = 'chorvachilik/chorva_category/list.html'

    def get(self, request, pk):
        qs = Chorvachilik.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('chorvachilik:chorva_category_list')
        else:
            return redirect('chorvachilik:chorva_category_list')


"""Generate EXCEL reports ↓ ↓ ↓ .xlsx files"""


class ChorvachilikXLSX(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/chorvachilik/chorvachilik/all/report/"""

    def get(self, request):
        from .excel.chorva import ChorvaSheet
        from .excel.poultry_report import PoultrySheet
        type_name = request.GET.get('type_name')
        start = request.GET.get('start')
        end = request.GET.get('end')
        if len(start) == 10 and len(end) == 10 and type_name:
            try:
                if type_name == "парранда бош сони" or "парранда" in type_name:
                    obj = ChorvachilikTypes.objects.get(name__iexact=type_name)
                    xlsx = PoultrySheet(user=self.request.user, obj=obj, start=start, end=end)
                    return xlsx.generate_poultry_excel_report()
                else:
                    obj = ChorvachilikTypes.objects.get(name__iexact=type_name)
                    xlsx = ChorvaSheet(user=self.request.user, obj=obj, start=start, end=end)
                    return xlsx.generate_cattle_report_by_type()
            except TreeTypes.DoesNotExist:
                raise Http404("Given query not found....")
        else:
            messages.error(request, "Sana noto'g'ri kiritilgan")
            return render(request, "chorvachilik/reports/regions_and_departments.html", {})


class ChorvaInputOutputXLSX(LoginRequiredMixin, View):
    """http://127.0.0.1:5000/chorvachilik/chorva/inp/out/report?department=97&end=2021-12-31"""

    def get(self, request):
        from ..chorvachilik.excel.input_output_report import ChorvaInputOutputSheet
        end = request.GET['end']
        department_pk = request.GET['department']
        if end and department_pk and len(end) == 10:
            try:
                obj = Department.objects.get(pk=department_pk)
                xlsx = ChorvaInputOutputSheet(user=self.request.user, end=end, obj=obj)
                return xlsx.generate_input_output_excel_report()
            except Department.DoesNotExist:
                raise Http404("Given query not found....")
        else:
            messages.error(request, "Sana noto'g'ri kiritilgan")
            return render(request, "chorvachilik/in_out_report/department.html", {})


class UploadFIleAPIView(APIView):
    def post(self, request):
        serializer = UploadFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {"id": serializer.data['id'], "file": serializer.data['file']}
        else:
            data = {"id": None, "file": None}
        return Response(data)


class UploadFIleDeleteAPIView(APIView):
    def get_object(self, pk):
        try:
            return UploadFile.objects.get(pk=pk)
        except UploadFile.DoesNotExist:
            raise Http404

    def post(self, request, pk) -> Response:
        img = self.get_object(pk)
        img.delete()
        return Response({"msg": "Deleted "}, status=status.HTTP_200_OK)
