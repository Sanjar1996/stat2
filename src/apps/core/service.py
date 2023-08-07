import datetime
import calendar

from django.core.serializers import serialize
from django.db.models import Sum

from ..accounts.models import UserDepartment
from ..finance.models import FinanceType, Finance, FinancePlan, ProductionServiceActual, ProductionServicePlan

epoch_year = datetime.date.today().year
current_month = datetime.date.today().month


def check_sum_is_none(_sum=None):
    total = 0
    if _sum:
        return int(_sum)
    else:
        return total


# BU FUNCTION USER QABUL QILADI VA SHU USERGA BOG"LANGAN REGION VA DEPARTMENTLARNI JSON QILIB QAYTARADI
def get_current_user_regions_and_departments_json(user=None):
    regions = None
    departments = None
    reg_and_depart = UserDepartment.objects.filter(user=user)
    for item_objects in reg_and_depart:
        regions = serialize('json', item_objects.regions.filter(status=1).order_by('sort'))
        departments = serialize('json', item_objects.departments.filter(status=1).order_by('sort'))
    if regions and departments:
        return regions, departments
    else:
        return None, None


# BU FUNCTION USER QABUL QILADI VA SHU USERGA BOG"LANGAN REGION VA DEPARTMENTLARNI QUERYSET QILIB QAYTARADI
def get_current_user_regions_and_departments_qs(user=None):
    regions = None
    departments = None
    reg_and_depart = UserDepartment.objects.filter(user=user)
    if reg_and_depart and len(reg_and_depart) > 0:
        regions = reg_and_depart[0].regions.filter(status=1).order_by('sort')
        departments = reg_and_depart[0].departments.filter(status=1).order_by('sort')

        return regions, departments
    else:
        return None, None


# PULLIK XIZMAT VA ISHLAB CHIQARISH DIAGRAMMASI UCHUN
def get_production_and_paid_service_data(user):
    regions, departments = get_current_user_regions_and_departments_qs(user)
    if regions and departments:
        actual_data = ProductionServiceActual.objects.filter(region__in=regions, date__year=epoch_year,
                                                             department__in=departments, status=1)
        plan_data = ProductionServicePlan.objects.filter(region__in=regions, date__year=epoch_year,
                                                         department__in=departments, status=1)
        production_plan_year_decimal = plan_data.aggregate(Sum('production'))
        service_plan_year_decimal = plan_data.aggregate(Sum('paid_service'))

        production_plan_year = check_sum_is_none(production_plan_year_decimal['production__sum'])
        service_plan_year = check_sum_is_none(service_plan_year_decimal['paid_service__sum'])

        prod_firs_quarter_decimal = actual_data.filter(date__quarter=1).aggregate(Sum('production'))
        prod_second_quarter_decimal = actual_data.filter(date__quarter=2).aggregate(Sum('production'))
        prod_tree_quarter_decimal = actual_data.filter(date__quarter=3).aggregate(Sum('production'))
        prod_four_quarter_decimal = actual_data.filter(date__quarter=4).aggregate(Sum('production'))

        prod_firs_quarter = check_sum_is_none(prod_firs_quarter_decimal['production__sum'])
        prod_second_quarter = check_sum_is_none(prod_second_quarter_decimal['production__sum'])
        prod_tree_quarter = check_sum_is_none(prod_tree_quarter_decimal['production__sum'])
        prod_four_quarter = check_sum_is_none(prod_four_quarter_decimal['production__sum'])

        ser_firs_quarter_decimal = actual_data.filter(date__quarter=1).aggregate(Sum('paid_service'))
        ser_second_quarter_decimal = actual_data.filter(date__quarter=2).aggregate(Sum('paid_service'))
        ser_tree_quarter_decimal = actual_data.filter(date__quarter=3).aggregate(Sum('paid_service'))
        ser_four_quarter_decimal = actual_data.filter(date__quarter=4).aggregate(Sum('paid_service'))

        ser_firs_quarter = check_sum_is_none(ser_firs_quarter_decimal['paid_service__sum'])
        ser_second_quarter = check_sum_is_none(ser_second_quarter_decimal['paid_service__sum'])
        ser_tree_quarter = check_sum_is_none(ser_tree_quarter_decimal['paid_service__sum'])
        ser_four_quarter = check_sum_is_none(ser_four_quarter_decimal['paid_service__sum'])
        result = [production_plan_year, prod_firs_quarter, prod_second_quarter, prod_tree_quarter, prod_four_quarter,
                  service_plan_year, ser_firs_quarter, ser_second_quarter, ser_tree_quarter, ser_four_quarter]
        ctx = {"production_and_paid_service": result}
    else:
        ctx = {"production_and_paid_service": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    return ctx


# MOLIYA TURLAIRDAN TUSHGAN DAROMAD XOZIRGI OYDA BOLGAN  FAQAT SHU OY UCHUN DIAGRAMMASI
def get_one_month_finance_types_income_sum(user):
    regions, departments = get_current_user_regions_and_departments_qs(user)
    if regions and departments:
        actual_month = []
        actual_data = Finance.objects.filter(region__in=regions,
                                             date__year=epoch_year,
                                             date__month=current_month,
                                             department__in=departments,
                                             status=1)
        finance_types = FinanceType.objects.filter(status=1)
        for type_name in finance_types:
            result_decimal = actual_data.filter(date__year=epoch_year,
                                                date__month=current_month,
                                                type=type_name).aggregate(Sum('amount'))
            result = check_sum_is_none(result_decimal['amount__sum'])
            actual_month.append(int(result))
        types = serialize('json', finance_types)
        if actual_month and types:
            context = {"actual_types": actual_month, "finance_types": types}
        else:
            context = {"actual_types": [], "finance_types": types}
        return context


# BU FUNCTION MOLIYA UCHUN YILLIK REJA VA AMALDAGILARNI QAYTARADI DIAGRAMMA UCHUN
def get_finance_actual_and_completed_sum(user):
    regions, departments = get_current_user_regions_and_departments_qs(user)
    if regions and departments:
        actual_year = []
        plan_year = []
        actual_data = Finance.objects.filter(region__in=regions, date__year=epoch_year, department__in=departments,
                                             status=1)
        plan_data = FinancePlan.objects.filter(region__in=regions, date__year=epoch_year, department__in=departments,
                                               status=1)
        for item in range(12):
            item = item + 1
            actual_sum_decimal = actual_data.filter(date__month=item).aggregate(Sum('amount'))
            actual_sum = check_sum_is_none(actual_sum_decimal['amount__sum'])
            actual_year.append(int(actual_sum))
            plan_sum_decimal = plan_data.filter(date__month=item).aggregate(Sum('amount'))
            plan_sum = check_sum_is_none(plan_sum_decimal['amount__sum'])
            plan_year.append(int(plan_sum))
        ctx = {"plan_year": plan_year, "actual_year": actual_year}
        return ctx
    else:
        ctx = {"plan_year": [], "actual_year": []}
        return ctx


# BU FUNCTION MOLIYA UCHUN XOZIRGI OYDA BOLGAN TUSHUMLARNI YANI AMALDAGILARNI QAYTARADI OYNI KUNLARINI DYNAMIC OLADI
def get_one_month_actual_and_plan_sum(user):
    regions, departments = get_current_user_regions_and_departments_qs(user)
    if regions and departments:
        actual_month = []
        actual_data = Finance.objects.filter(region__in=regions,
                                             date__year=epoch_year,
                                             date__month=current_month,
                                             department__in=departments,
                                             status=1)
        current_month_days_count = calendar.monthrange(epoch_year, current_month)[1]
        for item in range(current_month_days_count):
            item = item + 1
            result_decimal = actual_data.filter(date__year=epoch_year, date__month=current_month,
                                                date__day=item).aggregate(Sum('amount'))
            result = check_sum_is_none(result_decimal['amount__sum'])
            actual_month.append(int(result))
        context = {"actual_month": actual_month}
    else:
        context = {"actual_month": []}
    return context
