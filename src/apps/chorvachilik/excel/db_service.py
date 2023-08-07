from django.db.models import Sum
from ..models import ChorvachilikPlan, ChorvachilikActual
from ...accounts.models import UserDepartment


class CattleDBQuery:

    _type_id = ''
    _from = ''
    _to = ''

    def get_cattle_db_data(self, user, type_id, qs_category, start, end):
        self._type_id = type_id
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
                plan_act = []
                for category in qs_category:
                    _plan_act = tuple([
                        self.get_cattle_plan(dep_id=department.id, category_id=category.id),
                        self.get_cattle_actual(dep_id=department.id, category_id=category.id)],
                    )
                    plan_act.append(_plan_act)
                data['plan_act'] = plan_act
                all_data_department.append(data)
        return all_data_department

    def get_cattle_plan(self, dep_id, category_id):
        qs_plan = ChorvachilikPlan.objects.filter(
            chorvachilik_type_id=self._type_id, chorvachilik_id=category_id,
            department_id=dep_id,  date__range=[self._from, self._to],
            status=1).aggregate(Sum('amount'))
        return qs_plan['amount__sum'] if qs_plan['amount__sum'] else 0

    def get_cattle_actual(self, dep_id, category_id):
        qs_plan = ChorvachilikActual.objects.filter(
            chorvachilik_type_id=self._type_id, chorvachilik_id=category_id,
            department_id=dep_id,  date__year=self._from[:4],
            status=1).aggregate(Sum('amount'))
        return qs_plan['amount__sum'] if qs_plan['amount__sum'] else 0

