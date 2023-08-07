from django.db.models import Sum
from ..models import AgriculturePlan, AgricultureActual
from ...accounts.models import UserDepartment


class AgriculturalDBQuery:
    _from = ''
    _to = ''

    def get_agricultural_db_data(self, user, qs, start, end):
        self._from = start
        self._to = end
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
                qs_plan = AgriculturePlan.objects.filter(department_id=department.id, status=1)
                qs_act = AgricultureActual.objects.filter(department_id=department.id, status=1)
                plan = []
                act = []
                for item in qs:
                    agriculture_plan = qs_plan.filter(tree_type_id=item.id, date__range=[self._from, self._to])
                    hectare_plan = agriculture_plan.aggregate(Sum('hectare'))
                    weight_plan = agriculture_plan.aggregate(Sum('weight'))
                    _plan = tuple([hectare_plan['hectare__sum'] if hectare_plan['hectare__sum'] else 0,
                                   weight_plan['weight__sum'] if weight_plan['weight__sum'] else 0])

                    agriculture_act = qs_act.filter(tree_type_id=item.id, date__range=[self._from, self._to])
                    hectare_act = agriculture_act.aggregate(Sum('hectare'))
                    weight_act = agriculture_act.aggregate(Sum('weight'))
                    _act = tuple([hectare_act['hectare__sum'] if hectare_act['hectare__sum'] else 0,
                                   weight_act['weight__sum'] if weight_act['weight__sum'] else 0])
                    plan.append(_plan)
                    act.append(_act)
                data['plan'] = plan
                data['act'] = act
                all_data_department.append(data)
        return all_data_department

    def get_data_by_tree_type(self, user, cat_id, qs, start, end):
        print("QS...", qs, type(qs))
        self._from = start
        self._to = end
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
                qs_plan = AgriculturePlan.objects.filter(department_id=department.id, tree_type_id=cat_id, status=1)
                qs_act = AgricultureActual.objects.filter(department_id=department.id, tree_type_id=cat_id, status=1)
                plan = []
                act = []
                for item in qs:
                    agriculture_plan = qs_plan.filter(tree_plant_id=item.id, date__range=[self._from, self._to])
                    hectare_plan = agriculture_plan.aggregate(Sum('hectare'))
                    weight_plan = agriculture_plan.aggregate(Sum('weight'))
                    _plan = tuple([
                        hectare_plan['hectare__sum'] if hectare_plan['hectare__sum'] else 0,
                        weight_plan['weight__sum'] if weight_plan['weight__sum'] else 0])

                    agriculture_act = qs_act.filter(tree_plant_id=item.id, date__range=[self._from, self._to])
                    hectare_act = agriculture_act.aggregate(Sum('hectare'))
                    weight_act = agriculture_act.aggregate(Sum('weight'))
                    _act = tuple([
                        hectare_act['hectare__sum'] if hectare_act['hectare__sum'] else 0,
                        weight_act['weight__sum'] if weight_act['weight__sum'] else 0])
                    plan.append(_plan)
                    act.append(_act)
                data['plan'] = plan
                data['act'] = act
                all_data_department.append(data)
        return all_data_department

    # def get_agriculture_plan_hectare(self, dep, typ):
    #     qs_profit = AgriculturePlan.objects.filter(
    #         department_id=dep, tree_type_id=typ, status=1,
    #         date__gte=self._from, date__lt=self._to).aggregate(Sum('hectare'))
    #     return qs_profit['hectare__sum'] if qs_profit['hectare__sum'] else 0
    #
    # def get_agriculture_plan_weight(self, dep, typ):
    #     qs_weight = AgriculturePlan.objects.filter(
    #         department_id=dep, tree_type_id=typ, status=1,
    #         date__range=[self._from, self._to]).aggregate(Sum('weight'))
    #     return qs_weight['weight__sum'] if qs_weight['weight__sum'] else 0
    #
    # def get_agriculture_act_hectare(self, dep, typ):
    #     qs_profit = AgricultureActual.objects.filter(
    #         department_id=dep, tree_type_id=typ, status=1,
    #         date__gte=self._from, date__lt=self._to).aggregate(Sum('hectare'))
    #     return qs_profit['hectare__sum'] if qs_profit['hectare__sum'] else 0
    #
    # def get_agriculture_act_weight(self, dep, typ):
    #     qs_profit = AgricultureActual.objects.filter(
    #         department_id=dep, tree_type_id=typ, status=1,
    #         date__gte=self._from, date__lt=self._to).aggregate(Sum('weight'))
    #     return qs_profit['weight__sum'] if qs_profit['weight__sum'] else 0

