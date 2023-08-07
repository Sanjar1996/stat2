from django.db.models import Sum
import datetime
from ..models import Finance, FinancePlan, ProductionServicePlan, ProductionServiceActual
from ...accounts.models import UserDepartment


class DBQuery:
    TYPE: int = 0

    # QUARTER_1
    def quarter_1_month_1(self, user, end, at):
        self.TYPE = int(at)
        year = end[:4]
        month = end[5:7]
        qs_user_department = UserDepartment.objects.filter(user=user)
        all_data_department = []
        region_id = 0
        if qs_user_department.exists():
            departments = qs_user_department[0].departments.filter(status=1).order_by('sort')
            department_count = 0
            for item in departments:
                data = {'department': item.name, 'region_id': item.region.id}
                if region_id != item.region.id:
                    department_count = departments.filter(region_id=item.region.id).count()
                    region_id = item.region.id
                data['department_count'] = department_count
                year_plan = self.get_plan_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['year_plan'] = year_plan
                data['quarter_plan'] = self.get_plan_by_quarter(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter=1)
                data['daily_profit'] = self.get_daily_profit(dep_id=item.id, date=end)
                data['month_profit'] = self.get_profit_by_range(dep_id=item.id, year=year, month=month)
                plan_month_1 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-02-01')
                data['plan_month_1'] = plan_month_1
                act_month_1 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-02-01')
                data['act_month_1'] = act_month_1
                data['percent_month_1'] = self.calc_percent(plan=plan_month_1, act=act_month_1)
                tushum = self.get_actual_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['tushum'] = tushum
                data['annual_percent'] = self.calc_percent(plan=year_plan, act=tushum)
                all_data_department.append(data)
        return all_data_department

    def quarter_1_month_1_2(self, user, end, at):
        self.TYPE = int(at)
        year = end[:4]
        month = end[5:7]
        qs_user_department = UserDepartment.objects.filter(user=user)
        all_data_department = []
        region_id = 0
        if qs_user_department.exists():
            departments = qs_user_department[0].departments.filter(status=1).order_by('sort')
            department_count = 0
            for item in departments:
                data = {'department': item.name, 'region_id': item.region.id}
                if region_id != item.region.id:
                    department_count = departments.filter(region_id=item.region.id).count()
                    region_id = item.region.id
                data['department_count'] = department_count
                year_plan = self.get_plan_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['year_plan'] = year_plan
                data['quarter_plan'] = self.get_plan_by_quarter(dep_id=item.id, start=f'{year}-01-01',
                                                                  end=f'{year}-12-31', quarter=1)
                # ----------- 1-MONTH -----------
                plan_month_1 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-02-01')
                data['plan_month_1'] = plan_month_1
                act_month_1 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-02-01')
                data['act_month_1'] = act_month_1
                data['percent_month_1'] = self.calc_percent(plan=plan_month_1, act=act_month_1)
                # ----------- 2-MONTH -----------
                # print("D...", self.get_daily_profit(dep_id=item.id, date=end))
                data['daily_profit'] = self.get_daily_profit(dep_id=item.id, date=end)
                data['month_profit'] = self.get_profit_by_range(dep_id=item.id, year=year, month=month)
                plan_month_2 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-02-01', end=f'{year}-03-01')
                data['plan_month_2'] = plan_month_2
                act_month_2 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-02-01', end=f'{year}-03-01')
                data['act_month_2'] = act_month_2
                data['percent_month_2'] = self.calc_percent(plan=plan_month_2, act=act_month_2)
                tushum = self.get_actual_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['tushum'] = tushum
                data['annual_percent'] = self.calc_percent(plan=year_plan, act=tushum)
                all_data_department.append(data)
        return all_data_department

    def quarter_1_month_1_2_3(self, user, end, at):
        self.TYPE = int(at)
        year = end[:4]
        month = end[5:7]
        qs_user_department = UserDepartment.objects.filter(user=user)
        all_data_department = []
        region_id = 0
        if qs_user_department.exists():
            departments = qs_user_department[0].departments.filter(status=1).order_by('sort')
            department_count = 0
            for item in departments:
                data = {'department': item.name, 'region_id': item.region.id}
                if region_id != item.region.id:
                    department_count = departments.filter(region_id=item.region.id).count()
                    region_id = item.region.id
                data['department_count'] = department_count
                year_plan = self.get_plan_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['year_plan'] = year_plan
                data['quarter_plan'] = self.get_plan_by_quarter(dep_id=item.id, start=f'{year}-01-01',
                                                                  end=f'{year}-12-31', quarter=1)
                # ----------- 1-MONTH -----------
                plan_month_1 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-02-01')
                data['plan_month_1'] = plan_month_1
                act_month_1 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-02-01')
                data['act_month_1'] = act_month_1
                data['percent_month_1'] = self.calc_percent(plan=plan_month_1, act=act_month_1)
                # ----------- 2-MONTH -----------
                plan_month_2 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-02-01', end=f'{year}-03-01')
                data['plan_month_2'] = plan_month_2
                act_month_2 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-02-01', end=f'{year}-03-01')
                data['act_month_2'] = act_month_2
                data['percent_month_2'] = self.calc_percent(plan=plan_month_2, act=act_month_2)
                # ----------- 3-MONTH -----------
                # print("D...", self.get_daily_profit(dep_id=item.id, date=end))
                data['daily_profit'] = self.get_daily_profit(dep_id=item.id, date=end)
                data['month_profit'] = self.get_profit_by_range(dep_id=item.id, year=year, month=month)
                plan_month_3 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-03-01', end=f'{year}-04-01')
                data['plan_month_3'] = plan_month_3
                act_month_3 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-03-01', end=f'{year}-04-01')
                data['act_month_3'] = act_month_3
                data['percent_month_3'] = self.calc_percent(plan=plan_month_3, act=act_month_3)

                tushum = self.get_actual_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['tushum'] = tushum
                data['annual_percent'] = self.calc_percent(plan=year_plan, act=tushum)
                all_data_department.append(data)
        return all_data_department

    # QUARTER_2
    def quarter_2_month_1(self, user, end, at):
        self.TYPE = int(at)
        year = end[:4]
        month = end[5:7]
        qs_user_department = UserDepartment.objects.filter(user=user)
        all_data_department = []
        region_id = 0
        if qs_user_department.exists():
            departments = qs_user_department[0].departments.filter(status=1).order_by('sort')
            department_count = 0
            for item in departments:
                data = {'department': item.name, 'region_id': item.region.id}
                if region_id != item.region.id:
                    department_count = departments.filter(region_id=item.region.id).count()
                    region_id = item.region.id
                data['department_count'] = department_count
                year_plan = self.get_plan_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['year_plan'] = year_plan

                quarter_plan = self.get_plan_by_quarter(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter=1)
                data['quarter_plan'] = quarter_plan
                quarter_act = self.get_actual_by_quarter(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter=1)
                data['quarter_act'] = quarter_act
                data['quarter_1_percent'] = self.calc_percent(plan=quarter_plan, act=quarter_act)
                # ---------- 2-Quarter Plan ----------
                data['quarter_2_plan'] = self.get_plan_by_quarter(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter=2)
                # ---------- 4-MONTH ----------
                data['daily_profit'] = self.get_daily_profit(dep_id=item.id, date=end)
                data['month_profit'] = self.get_profit_by_range(dep_id=item.id, year=year, month=month)
                plan_month_4 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-04-01', end=f'{year}-05-01')
                data['plan_month_4'] = plan_month_4
                act_month_4 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-04-01', end=f'{year}-05-01')
                data['act_month_4'] = act_month_4
                data['percent_month_4'] = self.calc_percent(plan=plan_month_4, act=act_month_4)

                tushum = self.get_actual_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['tushum'] = tushum
                data['annual_percent'] = self.calc_percent(plan=year_plan, act=tushum)
                all_data_department.append(data)
        return all_data_department

    def quarter_2_month_1_2(self, user, end, at):
        self.TYPE = int(at)
        year = end[:4]
        month = end[5:7]
        qs_user_department = UserDepartment.objects.filter(user=user)
        all_data_department = []
        region_id = 0
        if qs_user_department.exists():
            departments = qs_user_department[0].departments.filter(status=1).order_by('sort')
            department_count = 0
            for item in departments:
                data = {'department': item.name, 'region_id': item.region.id}
                if region_id != item.region.id:
                    department_count = departments.filter(region_id=item.region.id).count()
                    region_id = item.region.id
                data['department_count'] = department_count
                year_plan = self.get_plan_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['year_plan'] = year_plan

                quarter_plan = self.get_plan_by_quarter(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter=1)
                data['quarter_plan'] = quarter_plan
                quarter_act = self.get_actual_by_quarter(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter=1)
                data['quarter_act'] = quarter_act
                data['quarter_1_percent'] = self.calc_percent(plan=quarter_plan, act=quarter_act)
                # ---------- 2-Quarter Plan ----------
                data['quarter_2_plan'] = self.get_plan_by_quarter(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter=2)
                # ---------- 4-MONTH ----------
                plan_month_4 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-04-01', end=f'{year}-05-01')
                data['plan_month_4'] = plan_month_4
                act_month_4 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-04-01', end=f'{year}-05-01')
                data['act_month_4'] = act_month_4
                data['percent_month_4'] = self.calc_percent(plan=plan_month_4, act=act_month_4)
                # ---------- 5-MONTH ----------
                data['daily_profit'] = self.get_daily_profit(dep_id=item.id, date=end)
                data['month_profit'] = self.get_profit_by_range(dep_id=item.id, year=year, month=month)
                plan_month_5 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-05-01', end=f'{year}-06-01')
                data['plan_month_5'] = plan_month_5
                act_month_5 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-05-01', end=f'{year}-06-01')
                data['act_month_5'] = act_month_5
                data['percent_month_5'] = self.calc_percent(plan=plan_month_5, act=act_month_5)

                tushum = self.get_actual_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['tushum'] = tushum
                data['annual_percent'] = self.calc_percent(plan=year_plan, act=tushum)
                all_data_department.append(data)
        return all_data_department

    def quarter_2_month_1_2_3(self, user, end, at):
        self.TYPE = int(at)
        year = end[:4]
        month = end[5:7]
        qs_user_department = UserDepartment.objects.filter(user=user)
        all_data_department = []
        region_id = 0
        if qs_user_department.exists():
            departments = qs_user_department[0].departments.filter(status=1).order_by('sort')
            department_count = 0
            for item in departments:
                data = {'department': item.name, 'region_id': item.region.id}
                if region_id != item.region.id:
                    department_count = departments.filter(region_id=item.region.id).count()
                    region_id = item.region.id
                data['department_count'] = department_count
                year_plan = self.get_plan_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')

                data['year_plan'] = year_plan
                quarter_plan = self.get_plan_by_quarter(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter=1)
                data['quarter_plan'] = quarter_plan
                quarter_act = self.get_actual_by_quarter(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter=1)
                data['quarter_act'] = quarter_act
                data['quarter_1_percent'] = self.calc_percent(plan=quarter_plan, act=quarter_act)
                # ---------- 2-Quarter Plan ----------
                data['quarter_2_plan'] = self.get_plan_by_quarter(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter=2)
                # ---------- 4-MONTH ----------
                plan_month_4 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-04-01', end=f'{year}-05-01')
                data['plan_month_4'] = plan_month_4
                act_month_4 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-04-01', end=f'{year}-05-01')
                data['act_month_4'] = act_month_4
                data['percent_month_4'] = self.calc_percent(plan=plan_month_4, act=act_month_4)
                # ---------- 5-MONTH ----------
                plan_month_5 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-05-01', end=f'{year}-06-01')
                data['plan_month_5'] = plan_month_5
                act_month_5 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-05-01', end=f'{year}-06-01')
                data['act_month_5'] = act_month_5
                data['percent_month_5'] = self.calc_percent(plan=plan_month_5, act=act_month_5)
                # ---------- 6-MONTH ----------
                data['daily_profit'] = self.get_daily_profit(dep_id=item.id, date=end)
                data['month_profit'] = self.get_profit_by_range(dep_id=item.id, year=year, month=month)
                plan_month_6 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-06-01', end=f'{year}-07-01')
                data['plan_month_6'] = plan_month_6
                act_month_6 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-06-01', end=f'{year}-07-01')
                data['act_month_6'] = act_month_6
                data['percent_month_6'] = self.calc_percent(plan=plan_month_6, act=act_month_6)

                tushum = self.get_actual_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['tushum'] = tushum
                data['annual_percent'] = self.calc_percent(plan=year_plan, act=tushum)
                all_data_department.append(data)
        return all_data_department

    # QUARTER_3
    def quarter_3_month_1(self, user, end, at):
        self.TYPE = int(at)
        year = end[:4]
        month = end[5:7]
        qs_user_department = UserDepartment.objects.filter(user=user)
        all_data_department = []
        region_id = 0
        if qs_user_department.exists():
            departments = qs_user_department[0].departments.filter(status=1).order_by('sort')
            department_count = 0
            for item in departments:
                data = {'department': item.name, 'region_id': item.region.id}
                if region_id != item.region.id:
                    department_count = departments.filter(region_id=item.region.id).count()
                    region_id = item.region.id
                data['department_count'] = department_count
                year_plan = self.get_plan_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['year_plan'] = year_plan
                quarter_plan = self.get_plan_by_quarter_range(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter_start=1, quarter_end=2)
                data['quarter_plan'] = quarter_plan
                quarter_act = self.get_actual_by_quarter_range(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter_start=1, quarter_end=2)
                data['quarter_act'] = quarter_act
                data['quarter_2_percent'] = self.calc_percent(plan=quarter_plan, act=quarter_act)
                # ---------- 3-Quarter Plan ----------
                data['quarter_3_plan'] = self.get_plan_by_quarter(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter=3)
                # ---------- 7-MONTH ----------
                data['daily_profit'] = self.get_daily_profit(dep_id=item.id, date=end)
                data['month_profit'] = self.get_profit_by_range(dep_id=item.id, year=year, month=month)
                plan_month_7 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-07-01', end=f'{year}-08-01')
                data['plan_month_7'] = plan_month_7
                act_month_7 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-07-01', end=f'{year}-08-01')
                data['act_month_7'] = act_month_7
                data['percent_month_7'] = self.calc_percent(plan=plan_month_7, act=act_month_7)

                tushum = self.get_actual_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['tushum'] = tushum
                data['annual_percent'] = self.calc_percent(plan=year_plan, act=tushum)
                all_data_department.append(data)
        return all_data_department

    def quarter_3_month_1_2(self, user, end, at):
        self.TYPE = int(at)
        year = end[:4]
        month = end[5:7]
        qs_user_department = UserDepartment.objects.filter(user=user)
        all_data_department = []
        region_id = 0
        if qs_user_department.exists():
            departments = qs_user_department[0].departments.filter(status=1).order_by('sort')
            department_count = 0
            for item in departments:
                data = {'department': item.name, 'region_id': item.region.id}
                if region_id != item.region.id:
                    department_count = departments.filter(region_id=item.region.id).count()
                    region_id = item.region.id
                data['department_count'] = department_count
                year_plan = self.get_plan_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['year_plan'] = year_plan
                quarter_plan = self.get_plan_by_quarter_range(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter_start=1, quarter_end=2)
                data['quarter_plan'] = quarter_plan
                quarter_act = self.get_actual_by_quarter_range(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter_start=1, quarter_end=2)
                data['quarter_act'] = quarter_act
                data['quarter_2_percent'] = self.calc_percent(plan=quarter_plan, act=quarter_act)
                # ---------- 3-Quarter Plan ----------
                data['quarter_3_plan'] = self.get_plan_by_quarter(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter=3)
                # ---------- 7-MONTH ----------
                plan_month_7 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-07-01', end=f'{year}-08-01')
                data['plan_month_7'] = plan_month_7
                act_month_7 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-07-01', end=f'{year}-08-01')
                data['act_month_7'] = act_month_7
                data['percent_month_7'] = self.calc_percent(plan=plan_month_7, act=act_month_7)
                # ---------- 8-MONTH ----------
                data['daily_profit'] = self.get_daily_profit(dep_id=item.id, date=end)
                data['month_profit'] = self.get_profit_by_range(dep_id=item.id, year=year, month=month)
                plan_month_8 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-08-01', end=f'{year}-09-01')
                data['plan_month_8'] = plan_month_8
                act_month_8 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-08-01', end=f'{year}-09-01')
                data['act_month_8'] = act_month_8
                data['percent_month_8'] = self.calc_percent(plan=plan_month_8, act=act_month_8)

                tushum = self.get_actual_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['tushum'] = tushum
                data['annual_percent'] = self.calc_percent(plan=year_plan, act=tushum)
                all_data_department.append(data)
        return all_data_department

    def quarter_3_month_1_2_3(self, user, end, at):
        self.TYPE = int(at)
        year = end[:4]
        month = end[5:7]
        qs_user_department = UserDepartment.objects.filter(user=user)
        all_data_department = []
        region_id = 0
        if qs_user_department.exists():
            departments = qs_user_department[0].departments.filter(status=1).order_by('sort')
            department_count = 0
            for item in departments:
                data = {'department': item.name, 'region_id': item.region.id}
                if region_id != item.region.id:
                    department_count = departments.filter(region_id=item.region.id).count()
                    region_id = item.region.id
                data['department_count'] = department_count
                year_plan = self.get_plan_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['year_plan'] = year_plan
                quarter_plan = self.get_plan_by_quarter_range(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter_start=1, quarter_end=2)
                data['quarter_plan'] = quarter_plan
                quarter_act = self.get_actual_by_quarter_range(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter_start=1, quarter_end=2)
                data['quarter_act'] = quarter_act
                data['quarter_2_percent'] = self.calc_percent(plan=quarter_plan, act=quarter_act)
                # ---------- 3-Quarter Plan ----------
                data['quarter_3_plan'] = self.get_plan_by_quarter(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter=3)
                # ---------- 7-MONTH ----------
                plan_month_7 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-07-01', end=f'{year}-08-01')
                data['plan_month_7'] = plan_month_7
                act_month_7 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-07-01', end=f'{year}-08-01')
                data['act_month_7'] = act_month_7
                data['percent_month_7'] = self.calc_percent(plan=plan_month_7, act=act_month_7)
                # ---------- 8-MONTH ----------
                plan_month_8 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-08-01', end=f'{year}-09-01')
                data['plan_month_8'] = plan_month_8
                act_month_8 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-08-01', end=f'{year}-09-01')
                data['act_month_8'] = act_month_8
                data['percent_month_8'] = self.calc_percent(plan=plan_month_8, act=act_month_8)
                # ---------- 9-MONTH ----------
                data['daily_profit'] = self.get_daily_profit(dep_id=item.id, date=end)
                data['month_profit'] = self.get_profit_by_range(dep_id=item.id, year=year, month=month)
                plan_month_9 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-09-01', end=f'{year}-10-01')
                data['plan_month_9'] = plan_month_9
                act_month_9 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-09-01', end=f'{year}-10-01')
                data['act_month_9'] = act_month_9
                data['percent_month_9'] = self.calc_percent(plan=plan_month_9, act=act_month_9)

                tushum = self.get_actual_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['tushum'] = tushum
                data['annual_percent'] = self.calc_percent(plan=year_plan, act=tushum)
                all_data_department.append(data)
        return all_data_department

    # QUARTER_4
    def quarter_4_month_1(self, user, end, at):
        self.TYPE = int(at)
        year = end[:4]
        month = end[5:7]
        qs_user_department = UserDepartment.objects.filter(user=user)
        all_data_department = []
        region_id = 0
        if qs_user_department.exists():
            departments = qs_user_department[0].departments.filter(status=1).order_by('sort')
            department_count = 0
            for item in departments:
                data = {'department': item.name, 'region_id': item.region.id}
                if region_id != item.region.id:
                    department_count = departments.filter(region_id=item.region.id).count()
                    region_id = item.region.id
                data['department_count'] = department_count
                year_plan = self.get_plan_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['year_plan'] = year_plan
                quarter_plan = self.get_plan_by_quarter_range(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter_start=1, quarter_end=3)
                data['quarter_plan'] = quarter_plan
                quarter_act = self.get_actual_by_quarter_range(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter_start=1, quarter_end=3)
                data['quarter_act'] = quarter_act
                data['quarter_3_percent'] = self.calc_percent(plan=quarter_plan, act=quarter_act)
                # ---------- 4-Quarter Plan ----------
                data['quarter_4_plan'] = self.get_plan_by_quarter(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter=4)
                # ---------- 10-MONTH ----------
                data['daily_profit'] = self.get_daily_profit(dep_id=item.id, date=end)
                data['month_profit'] = self.get_profit_by_range(dep_id=item.id, year=year, month=month)
                plan_month_10 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-10-01', end=f'{year}-11-01')
                data['plan_month_10'] = plan_month_10
                act_month_10 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-10-01', end=f'{year}-11-01')
                data['act_month_10'] = act_month_10
                data['percent_month_10'] = self.calc_percent(plan=plan_month_10, act=act_month_10)

                tushum = self.get_actual_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['tushum'] = tushum
                data['annual_percent'] = self.calc_percent(plan=year_plan, act=tushum)
                all_data_department.append(data)
        return all_data_department

    def quarter_4_month_1_2(self, user, end, at):
        self.TYPE = int(at)
        year = end[:4]
        month = end[5:7]
        qs_user_department = UserDepartment.objects.filter(user=user)
        all_data_department = []
        region_id = 0
        if qs_user_department.exists():
            departments = qs_user_department[0].departments.filter(status=1).order_by('sort')
            department_count = 0
            for item in departments:
                data = {'department': item.name, 'region_id': item.region.id}
                if region_id != item.region.id:
                    department_count = departments.filter(region_id=item.region.id).count()
                    region_id = item.region.id
                data['department_count'] = department_count
                year_plan = self.get_plan_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['year_plan'] = year_plan
                quarter_plan = self.get_plan_by_quarter_range(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter_start=1, quarter_end=3)
                data['quarter_plan'] = quarter_plan
                quarter_act = self.get_actual_by_quarter_range(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter_start=1, quarter_end=3)
                data['quarter_act'] = quarter_act
                data['quarter_3_percent'] = self.calc_percent(plan=quarter_plan, act=quarter_act)
                # ---------- 4-Quarter Plan ----------
                data['quarter_4_plan'] = self.get_plan_by_quarter(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter=4)
                # ---------- 10-MONTH ----------
                plan_month_10 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-10-01', end=f'{year}-11-01')
                data['plan_month_10'] = plan_month_10
                act_month_10 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-10-01', end=f'{year}-11-01')
                data['act_month_10'] = act_month_10
                data['percent_month_10'] = self.calc_percent(plan=plan_month_10, act=act_month_10)
                # ---------- 11-MONTH ----------
                data['daily_profit'] = self.get_daily_profit(dep_id=item.id, date=end)
                data['month_profit'] = self.get_profit_by_range(dep_id=item.id, year=year, month=month)
                plan_month_11 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-11-01', end=f'{year}-12-01')
                data['plan_month_11'] = plan_month_11
                act_month_11 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-11-01', end=f'{year}-12-01')
                data['act_month_11'] = act_month_11
                data['percent_month_11'] = self.calc_percent(plan=plan_month_11, act=act_month_11)

                tushum = self.get_actual_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['tushum'] = tushum
                data['annual_percent'] = self.calc_percent(plan=year_plan, act=tushum)
                all_data_department.append(data)
        return all_data_department

    def quarter_4_month_1_2_3(self, user, end, at):
        self.TYPE = int(at)
        year = end[:4]
        month = end[5:7]
        qs_user_department = UserDepartment.objects.filter(user=user)
        all_data_department = []
        region_id = 0
        if qs_user_department.exists():
            departments = qs_user_department[0].departments.filter(status=1).order_by('sort')
            department_count = 0
            for item in departments:
                data = {'department': item.name, 'region_id': item.region.id}
                if region_id != item.region.id:
                    department_count = departments.filter(region_id=item.region.id).count()
                    region_id = item.region.id
                data['department_count'] = department_count
                year_plan = self.get_plan_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['year_plan'] = year_plan
                quarter_plan = self.get_plan_by_quarter_range(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter_start=1, quarter_end=3)
                data['quarter_plan'] = quarter_plan
                quarter_act = self.get_actual_by_quarter_range(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter_start=1, quarter_end=3)
                data['quarter_act'] = quarter_act
                data['quarter_3_percent'] = self.calc_percent(plan=quarter_plan, act=quarter_act)
                # ---------- 4-Quarter Plan ----------
                data['quarter_4_plan'] = self.get_plan_by_quarter(
                    dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31', quarter=4)
                # ---------- 10-MONTH ----------
                plan_month_10 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-10-01', end=f'{year}-11-01')
                data['plan_month_10'] = plan_month_10
                act_month_10 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-10-01', end=f'{year}-11-01')
                data['act_month_10'] = act_month_10
                data['percent_month_10'] = self.calc_percent(plan=plan_month_10, act=act_month_10)
                # ---------- 11-MONTH ----------
                plan_month_11 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-11-01', end=f'{year}-12-01')
                data['plan_month_11'] = plan_month_11
                act_month_11 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-11-01', end=f'{year}-12-01')
                data['act_month_11'] = act_month_11
                data['percent_month_11'] = self.calc_percent(plan=plan_month_11, act=act_month_11)
                # ---------- 12-MONTH ----------
                data['daily_profit'] = self.get_daily_profit(dep_id=item.id, date=end)
                data['month_profit'] = self.get_profit_by_range(dep_id=item.id, year=year, month=month)
                plan_month_12 = self.get_plan_by_range(dep_id=item.id, start=f'{year}-12-01', end=f'{year}-12-31')
                data['plan_month_12'] = plan_month_12
                act_month_12 = self.get_actual_by_range(dep_id=item.id, start=f'{year}-12-01', end=f'{year}-12-31')
                data['act_month_12'] = act_month_12
                data['percent_month_12'] = self.calc_percent(plan=plan_month_12, act=act_month_12)

                tushum = self.get_actual_by_range(dep_id=item.id, start=f'{year}-01-01', end=f'{year}-12-31')
                data['tushum'] = tushum
                data['annual_percent'] = self.calc_percent(plan=year_plan, act=tushum)
                all_data_department.append(data)
        return all_data_department

    def get_plan_by_quarter_range(self, dep_id, start: str = '', end: str = '',
                                  quarter_start: int = 0, quarter_end: int = 0):
        quarter_plan = FinancePlan.objects.filter(
            department_id=dep_id,
            status=1, amount_type=self.TYPE,
            date__gte=start, date__lte=end,
            date__quarter__range=(quarter_start, quarter_end)).aggregate(Sum('amount'))
        return quarter_plan['amount__sum'] if quarter_plan['amount__sum'] else 0

    def get_actual_by_quarter_range(self, dep_id, start: str = '', end: str = '',
                                    quarter_start: int = 0, quarter_end: int = 0):
        quarter_plan = Finance.objects.filter(
            department_id=dep_id,
            status=1, state=2,
            amount_type=self.TYPE,
            date__gte=start, date__lte=end,
            date__quarter__range=(quarter_start, quarter_end)).aggregate(Sum('amount'))
        return quarter_plan['amount__sum'] if quarter_plan['amount__sum'] else 0

    def get_plan_by_quarter(self, dep_id, start: str = '', end: str = '', quarter: int = 0):
        quarter_plan = FinancePlan.objects.filter(
            department_id=dep_id,
            status=1, amount_type=self.TYPE,
            date__gte=start, date__lte=end,
            date__quarter=quarter).aggregate(Sum('amount'))
        return quarter_plan['amount__sum'] if quarter_plan['amount__sum'] else 0

    def get_actual_by_quarter(self, dep_id, start: str = '', end: str = '', quarter: int = 0):
        quarter_plan = Finance.objects.filter(
            department_id=dep_id,
            status=1, state=2,
            amount_type=self.TYPE,
            date__gte=start, date__lte=end,
            date__quarter=quarter).aggregate(Sum('amount'))
        return quarter_plan['amount__sum'] if quarter_plan['amount__sum'] else 0

    def get_daily_profit(self, dep_id, date):
        quarter_plan = Finance.objects.filter(
            department_id=dep_id,
            status=1, state=2,
            amount_type=self.TYPE, date=date).aggregate(Sum('amount'))
        return quarter_plan['amount__sum'] if quarter_plan['amount__sum'] else 0

    def get_profit_by_range(self, dep_id, year, month):
        quarter_plan = Finance.objects.filter(
            department_id=dep_id,
            status=1, state=2,
            amount_type=self.TYPE,
            date__year=year, date__month=month).aggregate(Sum('amount'))
        return quarter_plan['amount__sum'] if quarter_plan['amount__sum'] else 0

    def get_plan_by_range(self, dep_id, start: str = '', end: str = ''):
        qs_plan = FinancePlan.objects.filter(
            department_id=dep_id,
            status=1, amount_type=self.TYPE,
            date__gte=start, date__lt=end).aggregate(Sum('amount'))
        return qs_plan['amount__sum'] if qs_plan['amount__sum'] else 0

    def get_actual_by_range(self, dep_id, start: str = '', end: str = ''):
        qs_act = Finance.objects.filter(
            department_id=dep_id,
            status=1, state=2,
            amount_type=self.TYPE,
            date__gte=start, date__lt=end).aggregate(Sum('amount'))
        return qs_act['amount__sum'] if qs_act['amount__sum'] else 0

    @staticmethod
    def calc_percent(plan, act):
        if plan != 0 and act != 0:
            return round(act * 100 / plan)
        return 0


class FinanceDBQuery:
    TYPE: int = 0

    def get_finance_profit(self, user, qs, start, end, at):
        self.TYPE = int(at)
        qs_user_department = UserDepartment.objects.filter(user=user)
        all_data_department = []
        region_id = 0
        if qs_user_department.exists():
            departments = qs_user_department[0].departments.filter(status=1).order_by('sort')
            department_count = 0
            for department in departments:
                data = {'department': department.name, 'region_id': department.region.id}
                if region_id != department.region.id:
                    department_count = departments.filter(region_id=department.region.id).count()
                    region_id = department.region.id
                data['department_count'] = department_count
                profits = []
                for item in qs:
                    qs_profit = Finance.objects.filter(
                        department_id=department.id,
                        type_id=item.id,
                        status=1, state=2,
                        amount_type=self.TYPE,
                        date__gte=start, date__lt=end).aggregate(Sum('amount'))
                    amount = qs_profit['amount__sum'] if qs_profit['amount__sum'] else 0
                    profits.append(amount)
                data['profits'] = profits
                all_data_department.append(data)
        return all_data_department


class ProductionDBQuery:

    _from = ''
    _to = ''

    def get_db_production_data(self, user, start, end):
        self._from = start
        self._to = end
        qs_user_department = UserDepartment.objects.filter(user=user)
        all_data_department = []
        region_id = 0
        if qs_user_department.exists():
            departments = qs_user_department[0].departments.filter(status=1).order_by('sort')
            department_count = 0
            for department in departments:
                prod_data = {'department': department.name, 'region_id': department.region.id}
                if region_id != department.region.id:
                    department_count = departments.filter(region_id=department.region.id).count()
                    region_id = department.region.id
                prod_data['department_count'] = department_count

                prod_year_plan = self.forest_production_plan(dep_id=department.id)
                prod_actual = self.forest_production_act(dep_id=department.id)
                paid_year_plan = self.paid_services_plan(dep_id=department.id)
                paid_actual = self.paid_services_act(dep_id=department.id)

                prod_data['prod_year_plan'] = prod_year_plan
                prod_data['prod_actual'] = prod_actual
                prod_data['paid_year_plan'] = paid_year_plan
                prod_data['paid_actual'] = paid_actual

                prod_data['general_year_plan'] = prod_year_plan + paid_year_plan
                prod_data['general_actual'] = prod_actual + paid_actual

                all_data_department.append(prod_data)
        return all_data_department

    def forest_production_plan(self, dep_id):
        """ ProductionServicePlan model ..."""
        qs_plan = ProductionServicePlan.objects.filter(
            department_id=dep_id, date__year=self._from[:4], status=1).aggregate(Sum('production'))
        return qs_plan['production__sum'] if qs_plan['production__sum'] else 0

    def forest_production_act(self, dep_id):
        """ ProductionServiceActual model ..."""
        qs_actual = ProductionServiceActual.objects.filter(
            department_id=dep_id, date__range=[self._from, self._to], status=1).aggregate(Sum('production'))
        return qs_actual['production__sum'] if qs_actual['production__sum'] else 0

    def paid_services_plan(self, dep_id):
        """ ProductionServicePlan model ..."""
        qs_plan = ProductionServicePlan.objects.filter(
            department_id=dep_id, date__year=self._from[:4], status=1).aggregate(Sum('paid_service'))
        return qs_plan['paid_service__sum'] if qs_plan['paid_service__sum'] else 0

    def paid_services_act(self, dep_id):
        """ ProductionServiceActual model ..."""
        qs_actual = ProductionServiceActual.objects.filter(
            department_id=dep_id, date__range=[self._from, self._to], status=1).aggregate(Sum('paid_service'))
        return qs_actual['paid_service__sum'] if qs_actual['paid_service__sum'] else 0



