import json
import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.aggregates import ArrayAgg
from django.core.serializers import serialize
from django.db.models import Sum, Count
from django.http import Http404
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.base import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ReportKey, ReportGroup, Report, ReportValue, ReportKind
from .serializers import ReportKeysSerializer, ReportGroupSerializer
from ..accounts.models import Department, Region
from ..core.service import get_current_user_regions_and_departments_json, get_current_user_regions_and_departments_qs
from ..finance.forms import FilterForm
from ..finance.views import _check_sum_is_none
from rest_framework.generics import ListAPIView


class ReportCreate(View):
    template_name = 'report/create.html'

    def get(self, request):
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        report_id = self.request.GET.get('id', None)
        report = get_object_or_404(Report, id=report_id)
        first_group_data = ReportKey.objects.values('report_group_one_id', 'report_group_one__name') \
            .filter(report_id=report.id, status=1, value_type__in=[1, 2]) \
            .annotate(keys=Count('id')) \
            .order_by('report_group_one_id', 'report_group_one__name')
        header_data = []
        for first_gn in first_group_data:
            second_gruop_data = ReportKey.objects.values('report_group_two_id', 'report_group_two__name') \
                .filter(report_id=report.id,
                        report_group_one_id=first_gn['report_group_one_id'],
                        value_type__in=[1, 2],
                        status=1).annotate(keys=Count('id')).order_by()
            if second_gruop_data:
                second_group = []
                for second_gn in second_gruop_data:
                    keys_data = ReportKey.objects.filter(report_id=report.id,
                                                         report_group_one_id=first_gn['report_group_one_id'],
                                                         report_group_two_id=second_gn['report_group_two_id'],
                                                         value_type__in=[1, 2],
                                                         status=1).order_by('id')
                    keys = []
                    for key in keys_data:
                        keys.append({
                            "keyId": key.id,
                            "keyName": key.name,
                            "keyValue": None,
                            "keyType": key.value_type
                        })
                    second_group.append({
                        "secondGroupId": second_gn['report_group_two_id'],
                        "secondGroupName": second_gn['report_group_two__name'],
                        "keys": keys,
                        "keyLength": second_gn['keys']
                    })
                header_data.append({
                    "firstGroupId": first_gn['report_group_one_id'],
                    "firstGroupName": first_gn['report_group_one__name'],
                    "keyLength": first_gn['keys'],
                    "second_groups": second_group,
                })
            else:
                keys_data = ReportKey.objects.filter(report_id=report.id,
                                                     report_group_one_id=first_gn['report_group_one_id'],
                                                     value_type__in=[1, 2],
                                                     status=1).order_by('id')
                keys = []
                for key in keys_data:
                    keys.append({
                        "keyId": key.id,
                        "keyName": key.name,
                        "keyValue": None,
                        "keyType": key.value_type
                    })
                header_data.append({
                    "firstGroupId": first_gn['report_group_one_id'],
                    "firstGroupName": first_gn['report_group_one__name'],
                    "keys": keys
                })
        ctx = {"regions": regions, 'departments': departments,
               "report": report,
               "report_keys": json.dumps(header_data)}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        data_list = json.loads(data['items'])
        response_status = 200
        created_date = datetime.datetime.strptime(
            datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')
        if data and data_list:
            for item in data_list:
                for groups_key, groups_value in item.items():
                    if groups_key == 'second_groups':
                        for group_items in groups_value:
                            for group_item_key, group_item_value in group_items.items():
                                if group_item_key == 'keys':
                                    for group_key_item in group_item_value:
                                        double_value = None
                                        string_value = None
                                        if group_key_item['keyType'] == 1:
                                            double_value = group_key_item['keyValue']
                                        elif group_key_item['keyType'] == 2:
                                            string_value = group_key_item['keyValue']
                                        ReportValue.objects.create(
                                            report_id_id=data['report_id'],
                                            date=created_date,
                                            report_key_id=group_key_item['keyId'],
                                            department_id=data['department'],
                                            region_id=data['region'],
                                            double=double_value,
                                            string=string_value
                                        )
                                        response_status = 201
                                else:
                                    response_status = 200

                    elif groups_key == 'keys':
                        for key_items in groups_value:
                            double_value = None
                            string_value = None
                            if key_items['keyType'] == 1:
                                double_value = key_items['keyValue']
                            elif key_items['keyType'] == 2:
                                string_value = key_items['keyValue']
                            ReportValue.objects.create(
                                report_id_id=data['report_id'],
                                date=created_date,
                                report_key_id=key_items['keyId'],
                                department_id=data['department'],
                                region_id=data['region'],
                                double=double_value,
                                string=string_value
                            )
                            response_status = 201
                    else:
                        response_status = 200
            return render(request, self.template_name, status=response_status)
        else:
            return render(request, self.template_name, status=400)


class UpdateReport(View):
    template_name = 'report/update.html'

    def get(self, request):
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        print("regions", regions, "departments", departments)
        ct = self.request.GET.get('date', None)
        created_date = datetime.datetime.strptime(ct, '%Y-%m-%d %H:%M') - datetime.timedelta(hours=5)
        # docker ichidagi vaqt UTC bo'lganligi uchun
        report = get_object_or_404(Report, id=self.request.GET.get('id', None))
        region = self.request.GET.get('region', None)
        department = self.request.GET.get('department', None)

        first_group_data = ReportKey.objects.values('report_group_one_id', 'report_group_one__name') \
            .filter(report_id=report.id, status=1, value_type__in=[1, 2]) \
            .annotate(keys=Count('id')) \
            .order_by('report_group_one_id', 'report_group_one__name')
        header_data = []
        for first_gn in first_group_data:
            second_gruop_data = ReportKey.objects.values('report_group_two_id', 'report_group_two__name') \
                .filter(report_id=report.id,
                        report_group_one_id=first_gn['report_group_one_id'],
                        value_type__in=[1, 2],
                        status=1).annotate(keys=Count('id')).order_by()
            if second_gruop_data:
                second_group = []
                for second_gn in second_gruop_data:
                    keys_data = ReportKey.objects.filter(report_id=report.id,
                                                         report_group_one_id=first_gn['report_group_one_id'],
                                                         report_group_two_id=second_gn['report_group_two_id'],
                                                         value_type__in=[1, 2],
                                                         status=1).order_by('id')
                    keys = []
                    for key in keys_data:
                        val = None
                        if key.value_type == 1:
                            report_value = ReportValue.objects.get(report_id=report.id, date=created_date,
                                                                   region_id=region,
                                                                   department_id=department, report_key=key)
                            val = report_value.double
                        elif key.value_type == 2:
                            report_value = ReportValue.objects.get(report_id=report.id, date=created_date,
                                                                   region_id=region,
                                                                   department_id=department, report_key=key)
                            val = report_value.string
                        keys.append({
                            "keyId": key.id,
                            "keyName": key.name,
                            "keyValue": str(val),
                            "keyType": key.value_type,
                            "valueId": report_value.id
                        })
                    second_group.append({
                        "secondGroupId": second_gn['report_group_two_id'],
                        "secondGroupName": second_gn['report_group_two__name'],
                        "keys": keys,
                        "keyLength": second_gn['keys']
                    })
                header_data.append({
                    "firstGroupId": first_gn['report_group_one_id'],
                    "firstGroupName": first_gn['report_group_one__name'],
                    "keyLength": first_gn['keys'],
                    "second_groups": second_group,
                })
            else:
                keys_data = ReportKey.objects.filter(report_id=report.id,
                                                     report_group_one_id=first_gn['report_group_one_id'],
                                                     value_type__in=[1, 2],
                                                     status=1).order_by('id')
                keys = []
                for key in keys_data:
                    if key.value_type == 1:
                        report_value = ReportValue.objects.get(report_id=report.id, date=created_date,
                                                               region_id_id=region,
                                                               department_id=department, report_key=key)
                        val = report_value.double
                    elif key.value_type == 2:
                        report_value = ReportValue.objects.get(report_id=report.id, date=created_date,
                                                               region_id_id=region,
                                                               department_id=department, report_key=key).string
                        val = report_value.string
                    keys.append({
                        "keyId": key.id,
                        "keyName": key.name,
                        "keyValue": str(val),
                        "keyType": key.value_type,
                        "valueId": report_value.id
                    })
                header_data.append({
                    "firstGroupId": first_gn['report_group_one_id'],
                    "firstGroupName": first_gn['report_group_one__name'],
                    "keys": keys
                })
        ctx = {"regions": regions, 'departments': departments,
               "report": report,
               "report_keys": json.dumps(header_data)}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        data_list = json.loads(data['items'])
        response_status = 200
        if data and data_list:
            for item in data_list:
                for groups_key, groups_value in item.items():
                    if groups_key == 'second_groups':
                        for group_items in groups_value:
                            for group_item_key, group_item_value in group_items.items():
                                if group_item_key == 'keys':
                                    for group_key_item in group_item_value:
                                        double_value = 0
                                        string_value = None
                                        if group_key_item['keyType'] == 1:
                                            double_value = group_key_item['keyValue']
                                        elif group_key_item['keyType'] == 2:
                                            string_value = group_key_item['keyValue']
                                        ReportValue.objects.filter(
                                            id=group_key_item['valueId'],
                                            report_id_id=data['report_id'],
                                            report_key_id=group_key_item['keyId']
                                        ).update(string=string_value, double=double_value)
                                        response_status = 201
                                else:
                                    response_status = 200

                    elif groups_key == 'keys':
                        for key_items in groups_value:
                            double_value = 0
                            string_value = None
                            if key_items['keyType'] == 1:
                                double_value = key_items['keyValue']
                            elif key_items['keyType'] == 2:
                                string_value = key_items['keyValue']
                            ReportValue.objects.filter(
                                id=key_items['valueId'],
                                report_id_id=data['report_id'],
                                report_key_id=key_items['keyId']
                            ).update(double=double_value, string=string_value)
                            response_status = 201
                    else:
                        response_status = 200
            # return render(request, self.template_name, status=response_status)
            return redirect("report:report_list")
        else:
            return render(request, self.template_name, status=400)


def check_first_group_id(gid=None, data_list=None):
    result = False
    if data_list:
        mylist = data_list[0]
        for key, val in mylist.items():
            if val == gid:
                result = True
                break
            else:
                continue
        return result
    else:
        return result


def check_second_group_id(gid=None, begin=0, data_list=None):
    result = False
    if data_list and 'second_groups' in data_list:
        mylist = data_list[begin]
        for item in mylist['second_groups']:
            if item['secondGroupId'] == gid:
                result = True
                break
            else:
                continue
        return result
    else:
        return result


def _check_first_group_id_in_list(gid=None, begin=None, data_list=None):
    mylist = data_list[begin]
    result = False
    if mylist:
        for key, val in mylist.items():
            if val == gid:
                result = True
                break
            else:
                continue
        return result
    else:
        return result


def _check_second_group_id_in_list(gid=None, begin=None, data_list=None):
    mylist = data_list[begin]
    result = False
    if mylist and 'second_groups' in data_list:
        for item in mylist['second_groups']:
            if item['secondGroupId'] == gid:
                result = True
                break
            else:
                continue
        return result
    else:
        return result


class ReportList(LoginRequiredMixin, ListView):
    model = Report
    context_object_name = 'object_list'
    template_name = 'report/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ReportList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = Report.objects.filter(status=1)
        return queryset


class ReportDetailView(ListView):
    model = ReportValue
    context_object_name = 'object_list'
    template_name = 'report/detail_list.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(ReportDetailView, self).get_context_data(**kwargs)
        context['report_id'] = self.request.GET.get('id', '')
        context['report'] = Report.objects.get(id=self.request.GET.get('id', ''))
        return context

    def get_queryset(self):
        report = Report.objects.get(id=self.request.GET.get('id'))
        reportkeys = ReportKey.objects.filter(report__id=self.request.GET.get('id'))
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        queryset = []
        if regions and departments:
            if report.kind == ReportKind.SUMMARY:
                queryset = ReportValue.objects.values("department_id", 'department__name', "region_id",
                                                      'region_id__name', 'date') \
                    .filter(report_key__in=reportkeys, region__in=regions, department__in=departments) \
                    .annotate(rcount=Count('region_id')).annotate(dcount=Count('department')) \
                    .annotate(d=Count('date')).order_by()
                # print(queryset)
                return queryset
            elif report.kind == ReportKind.LISTED:
                queryset = ReportValue.objects.values("department_id", 'department__name', "region_id",
                                                      'region_id__name', 'date').filter(
                    report_key__in=reportkeys, region__in=regions,
                    department__in=departments) \
                    .annotate(rcount=Count('region_id')).annotate(dcount=Count('department')).order_by()
                return queryset
        else:
            queryset = []
        return queryset


class ReportPageView(LoginRequiredMixin, View):
    template_name = 'report/hisobot/region_and_departments.html'

    def get(self, request, pk):
        current_year = datetime.date.today().year
        end_date = datetime.date(current_year, 12, 31).strftime('%Y-%m-%d')
        end = self.request.GET.get('end', None)
        if not end:
            end_dateformat = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            current_year = end_dateformat.year
            start = datetime.date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = datetime.date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.datetime.strptime(end, '%Y-%m-%d')
            current_year = end_dateformat.year
            start = datetime.date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = end_dateformat.strftime('%Y-%m-%d')
        report = get_object_or_404(Report, id=pk)
        if report.kind == ReportKind.SUMMARY:
            form = FilterForm(initial={"start": start, "end": end})
            first_group_data = ReportKey.objects.values('report_group_one_id', 'report_group_one__name') \
                .filter(report_id=report.id, status=1) \
                .annotate(keys=Count('id')) \
                .order_by('report_group_one_id', 'report_group_one__name')
            count = 0
            header_data = []

            for first_gn in first_group_data:
                second_gruop_data = ReportKey.objects.values('report_group_two_id', 'report_group_two__name') \
                    .filter(report_id=report.id,
                            report_group_one_id=first_gn['report_group_one_id'],
                            status=1).annotate(keys=Count('id')).order_by()
                if second_gruop_data:
                    second_group = []
                    for second_gn in second_gruop_data:
                        keys_data = ReportKey.objects.filter(report_id=report.id,
                                                             report_group_one_id=first_gn['report_group_one_id'],
                                                             report_group_two_id=second_gn['report_group_two_id'],
                                                             status=1).order_by('sort')
                        keys = []
                        for key in keys_data:
                            keys.append({
                                "keyId": key.id,
                                "keyName": key.name,
                                "keyValue": None
                            })
                        second_group.append({
                            "secondGroupId": second_gn['report_group_two_id'],
                            "secondGroupName": second_gn['report_group_two__name'],
                            "keys": keys,
                            "keyLength": second_gn['keys']
                        })
                    header_data.append({
                        "firstGroupId": first_gn['report_group_one_id'],
                        "firstGroupName": first_gn['report_group_one__name'],
                        "keyLength": first_gn['keys'],
                        "second_groups": second_group,
                    })
                else:
                    keys_data = ReportKey.objects.filter(report_id=report.id,
                                                         report_group_one_id=first_gn['report_group_one_id'],
                                                         status=1).order_by('sort')
                    keys = []
                    for key in keys_data:
                        keys.append({
                            "keyId": key.id,
                            "keyName": key.name,
                            "keyValue": None
                        })
                    header_data.append({
                        "firstGroupId": first_gn['report_group_one_id'],
                        "firstGroupName": first_gn['report_group_one__name'],
                        "keys": keys
                    })
            regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
            data = []
            region_id = None
            region_obj = None
            if regions and departments:
                report = Report.objects.get(id=pk)
                report_keys = ReportKey.objects.filter(report=report, status=1).order_by('sort')
                x = 1
                for depart in departments:
                    department_result = []
                    for key in report_keys:
                        if key.value_type == 3:
                            json_data = json.loads(key.query_code)
                            result = _solve_department(json_data, depart)
                            department_result.append(result)
                        else:
                            depart_query = ReportValue.objects.filter(department=depart, report_key=key,
                                                                      status=1).aggregate(Sum('double'))
                            department_result.append(_check_sum_is_none(depart_query['double__sum']))
                    if region_id != depart.region_id:
                        region_result = []
                        region_obj = Region.objects.get(id=depart.region_id)
                        for key in report_keys:
                            if key.value_type == 3:
                                json_data = json.loads(key.query_code.replace("'", '"'))
                                result = _solve_region(json_data, region_obj)
                                region_result.append(result)
                            else:
                                region_query = ReportValue.objects.filter(region=region_obj, report_key=key,
                                                                          status=1).aggregate(Sum('double'))
                                region_result.append(_check_sum_is_none(region_query['double__sum']))
                        data.append({
                            "index": 1,
                            "region_name": region_obj.name,
                            "region_result": region_result,
                            "depart_name": depart.name,
                            "department_result": department_result
                        })
                        x = 1
                    else:
                        data.append({
                            "index": x,
                            "depart_name": depart.name,
                            "department_result": department_result,
                        })

                    region_id = depart.region_id
                context = {"data": data, "form": form, "groups": json.dumps(header_data), "report": report,
                           "start": start, "end": end}
            else:
                context = {"data": data, "form": form, "groups": json.dumps(header_data), "report": report,
                           "start": start, "end": end}
            return render(request, self.template_name, context)
        elif report.kind == ReportKind.LISTED:
            self.template_name = 'report/hisobot/listed_report.html'
            regions_json, departments_json = get_current_user_regions_and_departments_json(self.request.user)
            first_group_data = ReportKey.objects.values('report_group_one_id', 'report_group_one__name') \
                .filter(report_id=report.id, status=1) \
                .annotate(keys=Count('id')) \
                .order_by('report_group_one_id', 'report_group_one__name')
            count = 0
            header_data = []
            for first_gn in first_group_data:
                second_gruop_data = ReportKey.objects.values('report_group_two_id', 'report_group_two__name') \
                    .filter(report_id=report.id,
                            report_group_one_id=first_gn['report_group_one_id'],
                            status=1).annotate(keys=Count('id')).order_by()
                if second_gruop_data:
                    second_group = []
                    for second_gn in second_gruop_data:
                        keys_data = ReportKey.objects.filter(report_id=report.id,
                                                             report_group_one_id=first_gn['report_group_one_id'],
                                                             report_group_two_id=second_gn['report_group_two_id'],
                                                             status=1).order_by('sort')
                        keys = []
                        for key in keys_data:
                            keys.append({
                                "keyId": key.id,
                                "keyName": key.name,
                                "keyValue": None
                            })
                        second_group.append({
                            "secondGroupId": second_gn['report_group_two_id'],
                            "secondGroupName": second_gn['report_group_two__name'],
                            "keys": keys,
                            "keyLength": second_gn['keys']
                        })
                    header_data.append({
                        "firstGroupId": first_gn['report_group_one_id'],
                        "firstGroupName": first_gn['report_group_one__name'],
                        "keyLength": first_gn['keys'],
                        "second_groups": second_group,
                    })
                else:
                    keys_data = ReportKey.objects.filter(report_id=report.id,
                                                         report_group_one_id=first_gn['report_group_one_id'],
                                                         status=1).order_by('sort')
                    keys = []
                    for key in keys_data:
                        keys.append({
                            "keyId": key.id,
                            "keyName": key.name,
                            "keyValue": None
                        })
                    header_data.append({
                        "firstGroupId": first_gn['report_group_one_id'],
                        "firstGroupName": first_gn['report_group_one__name'],
                        "keys": keys
                    })
            print("departments_json", departments_json)
            context = {"groups": json.dumps(header_data),
                       "regions": regions_json, "departments": departments_json,
                       "report": report,
                       "start": start, "end": end}
        else:
            context = {"start": start, "end": end}
        return render(request, self.template_name, context)


class ReportValueDelete(LoginRequiredMixin, View):
    template_name = 'report/detail_list.html'

    def post(self, request, pk):
        qs = ReportValue.objects.filter(id=pk)
        if qs.exists():
            qs.update(status=2)
            return render(request, template_name='report/detail_list.html', context={"id": qs[0].report_id})
        else:
            return JsonResponse({"msg": 'Error'})


class DevelopmentExcelReportView(View):
    """http://127.0.0.1:8000/trees/excel/page"""

    def get(self, request):
        return render(request, 'excel.html', {})


class CreateReportQuery(View):
    template_name = 'report/generateQuery.html'

    def get(self, request):
        reports = serialize('json', Report.objects.filter(status=1))
        groups = serialize('json', ReportGroup.objects.filter(status=1))
        ctx = {"reports": reports, "groups": groups}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        first = _get_report_group(data['firstGroupId'])
        second = _get_report_group(data['secondGroupId'])
        ReportKey.objects.create(name=data['reportKeyName'],
                                 report_id=data['report'],
                                 query_code=data['items'],
                                 report_group_one=first,
                                 report_group_two=second,
                                 sort=data['sortValue'],
                                 value_type=3)
        return JsonResponse({"message": True})


class ResponseReportKeys(ListAPIView):
    """Bu API report create page da report tanlasa AJAX
        qilib shu report ga bo'g'langan reportKey larni qaytarishi uchun
    """
    queryset = ReportKey.objects.all()
    serializer_class = ReportKeysSerializer

    def get_queryset(self):
        # return ReportKey.objects.filter(report=self.kwargs['pk'], value_type__in=[1, 2])
        # return ReportKey.objects.filter(report=self.kwargs['pk'])
        # XOZIRCHA BU XAMMASINI QAYTARYABDI MIXIN REPORT CREATE QILISH UCHUN
        return ReportKey.objects.filter(report_id=self.kwargs['pk']).exclude(value_type=3)


class GeneralDynamicReportXLSX(View):
    def get(self, request):
        from .excel.dynamic_report import DynamicExcelReport
        start = request.GET.get('start')
        end = request.GET.get('end')
        report_id = request.GET.get('report_id')
        if start and end and report_id:
            try:
                obj = Report.objects.get(id=report_id)
                xlsx = DynamicExcelReport(user=self.request.user, obj=obj, start=start, end=end)
                return xlsx.generate_dynamic_excel_report()
            except Report.DoesNotExist:
                raise Http404("Given query not found....")
        else:
            messages.error(request, f"Sana noto'g'ri kiritilgan, yoki `{report_id}` report mavjud emas!")
            return render(request, 'report/hisobot/region_and_departments.html', {})


actions = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "%": lambda x, y: (y % x) / x * 100,
}


def _solve_region(json_data=None, reg=None):
    current_qs = ReportValue.objects.filter(report_key_id=json_data[0]["reportKeyId"],
                                            region=reg, status=1).aggregate(Sum('double'))
    current = 0
    if current_qs['double__sum'] and current_qs['double__sum'] > 0:
        current = _check_sum(current_qs['double__sum'])
    else:
        current = _check_sum(json_data[0]["reportValue"])
    for i in range(len(json_data) - 1):
        action = actions[json_data[i]["actionValue"]]

        next_qs = ReportValue.objects.filter(report_key_id=json_data[i + 1]["reportKeyId"],
                                             region=reg, status=1).aggregate(Sum('double'))
        next_value = 0
        if next_qs['double__sum'] and next_qs['double__sum'] > 0:
            next_value = _check_sum(next_qs['double__sum'])
        else:
            next_value = _check_sum(json_data[i + 1]["reportValue"])
        try:
            current = action(float(current), float(next_value))
        except:
            current = 0
    return current


def _solve_department(json_data=None, depart=None):
    current_qs = ReportValue.objects.filter(report_key_id=json_data[0]["reportKeyId"],
                                            department=depart, status=1).aggregate(Sum('double'))
    current = 0
    if current_qs['double__sum'] and current_qs['double__sum'] > 0:
        current = _check_sum(current_qs['double__sum'])
    else:
        current = _check_sum(json_data[0]["reportValue"])
    for i in range(len(json_data) - 1):
        action = actions[json_data[i]["actionValue"]]
        next_qs = ReportValue.objects.filter(report_key_id=json_data[i + 1]["reportKeyId"],
                                             department=depart, status=1).aggregate(Sum('double'))
        next_value = 0
        if next_qs['double__sum'] and next_qs['double__sum'] > 0:
            next_value = _check_sum(next_qs['double__sum'])
        else:
            next_value = _check_sum(json_data[i + 1]["reportValue"])
        try:
            current = action(float(current), float(next_value))
        except:
            current = 0
        # current = action(current, next_value)
    return current


def _get_report_group(idd=None):
    try:
        group = ReportGroup.objects.get(id=idd)
        return group
    except:
        return None


def _check_sum(_sum=None):
    total = 0
    if _sum != 'None' and _sum:
        return float(_sum)
    else:
        return total


class CreateReportGroup(APIView):
    def post(self, request):
        data = request.POST
        if data['item']:
            report_group = ReportGroup.objects.create(name=data['item'])
            serializer = ReportGroupSerializer(report_group)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"msg": 'Error'})


class CreateNewReport(View):
    template_name = 'report/create_new_report.html'

    def get(self, request):
        groups = serialize('json', ReportGroup.objects.filter(status=1))
        ctx = {"groups": groups}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        items = json.loads(data['items'])
        if data:
            report = Report.objects.create(name=data['newReport'], type=data['reportType'], kind=data['reportKind'])
            if items:
                for item in items:
                    if item['valueType'] and item['reportKey']:
                        ReportKey.objects.create(report=report, report_group_one_id=item['reportGroupOne'],
                                                 report_group_two_id=item['reportGroupTwo'],
                                                 value_type=item['valueType'],
                                                 sort=item['sortValue'],
                                                 name=item['reportKey'])
                return JsonResponse({'msg': 'Success'})
            return JsonResponse({'msg': "Success"})
        else:
            return JsonResponse({'msg': 'Error'})


def get_listed_report_values(request):
    department_id = None
    year = None
    report_id = None
    results = []
    if request.method == 'GET':
        year = request.GET.get('y', None)
        department_id = request.GET.get('d', None)
        report_id = request.GET.get('r', None)
    department = Department.objects.get(id=department_id)
    if all((department, report_id, department_id, year)):
        report = Report.objects.get(id=report_id)
        report_keys = ReportKey.objects.filter(report=report, status=1).order_by('sort')
        values = ReportValue.objects.filter(report_id=report, department=department, date__year=year)
        if values.exists():
            if len(report_keys) == len(values):
                array_one = []
                for value in values:
                    if value.report_key.value_type == 1:
                        array_one.append({"value": value.double})
                    elif value.report_key.value_type == 2:
                        array_one.append({"value": value.string})
                    elif value.report_key.value_type == 3:
                        array_one.append({"value": ""})
                results.append(array_one)
            else:
                arr_length = 1
                array = []
                for value in values:
                    if arr_length == 1:
                        if value.report_key.value_type == 1:
                            array.append({"value": value.double})
                        elif value.report_key.value_type == 2:
                            array.append({"value": value.string})
                        elif value.report_key.value_type == 3:
                            array.append("")
                        arr_length += 1
                    elif len(report_keys) > arr_length:
                        if value.report_key.value_type == 1:
                            array.append({"value": value.double})
                        elif value.report_key.value_type == 2:
                            array.append({"value": value.string})
                        elif value.report_key.value_type == 3:
                            array.append({"value": ""})
                        arr_length += 1
                    elif len(report_keys) == arr_length:
                        if value.report_key.value_type == 1:
                            array.append({"value": value.double})
                        elif value.report_key.value_type == 2:
                            array.append({"value": value.string})
                        elif value.report_key.value_type == 3:
                            array.append({"value": ""})
                        arr_length = 1
                        results.append(array)
                        array = []
        else:
            return JsonResponse({"data": []}, status=status.HTTP_200_OK)
    return JsonResponse({"data": results}, status=status.HTTP_200_OK)


def _solve_lined_report(json_data=None, depart=None):
    current_qs = ReportValue.objects.filter(report_key_id=json_data[0]["reportKeyId"],
                                            department=depart, status=1).aggregate(Sum('double'))
    current = 0
    if current_qs['double__sum'] and current_qs['double__sum'] > 0:
        current = _check_sum(current_qs['double__sum'])
    else:
        current = _check_sum(json_data[0]["reportValue"])
    for i in range(len(json_data) - 1):
        action = actions[json_data[i]["actionValue"]]
        next_qs = ReportValue.objects.filter(report_key_id=json_data[i + 1]["reportKeyId"],
                                             department=depart, status=1).aggregate(Sum('double'))
        next_value = 0
        if next_qs['double__sum'] and next_qs['double__sum'] > 0:
            next_value = _check_sum(next_qs['double__sum'])
        else:
            next_value = _check_sum(json_data[i + 1]["reportValue"])
        try:
            current = action(float(current), float(next_value))
        except:
            current = 0
        # current = action(current, next_value)
    return current
