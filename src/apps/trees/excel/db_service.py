from django.db.models import Sum
from ..models import TreeContractCategory, TreeContract, TreeContractPlan, SaplingPlan, Sapling
from ...accounts.models import UserDepartment


class DBQuery:

    _from = ''
    _to = ''

    def get_all_tree_contracts(self, user, start, end):
        self._from = start
        self._to = end
        qs_user_department = UserDepartment.objects.filter(user=user)
        all_data_department = []
        region_id = 0
        qs_contract_category = TreeContractCategory.objects.filter(status=1).order_by('id')
        if qs_user_department.exists():
            departments = qs_user_department[0].departments.filter(status=1).order_by('sort')
            department_count = 0
            for department in departments:
                data = {'department': department.name, 'region_id': department.region.id}
                if region_id != department.region.id:
                    department_count = departments.filter(region_id=department.region.id).count()
                    region_id = department.region.id
                data['department_count'] = department_count
                year = start[:4]
                qs_plan = TreeContractPlan.objects.filter(
                    department_id=department, date__year=year, status=1).aggregate(Sum('tree_count'))
                data['year_plan'] = qs_plan['tree_count__sum'] if qs_plan['tree_count__sum'] else 0
                actual = tuple()
                for category in qs_contract_category:
                    actual += (self.get_actual_by_category(cat_id=category.id, dep_id=department.id, field='count'),)
                    actual += (self.get_actual_by_category(cat_id=category.id, dep_id=department.id, field='amount'),)
                    actual += (self.get_actual_by_category(cat_id=category.id, dep_id=department.id, field='payout'),)
                    actual += (self.get_actual_by_category(cat_id=category.id, dep_id=department.id, field='output_tree'),)
                data['actual'] = actual
                all_data_department.append(data)
        return all_data_department

    def get_actual_by_category(self, cat_id, dep_id, field):
        qs_plan = TreeContract.objects.filter(
            category_id=cat_id, department_id=dep_id,
            date__gte=self._from, date__lte=self._to, status=1).aggregate(Sum(str(field)))
        return qs_plan[f'{field}__sum'] if qs_plan[f'{field}__sum'] else 0


class TreePlantQuery:
    # _from = ''
    # _to = ''
    #
    # def get_tree_plan_data(self, user, start, end, qs):
    #     self._from = start
    #     self._to = end
    #     qs_user_department = UserDepartment.objects.filter(user=user)
    #     all_data_department = []
    #     region_id = 0
    #     if qs_user_department.exists():
    #         departments = qs_user_department[0].departments.filter(status=1).order_by('sort')
    #         department_count = 0
    #         for department in departments:
    #             data = {'department': department.name, 'region_id': department.region.id}
    #             if region_id != department.region.id:
    #                 department_count = departments.filter(region_id=department.region.id).count()
    #                 region_id = department.region.id
    #             data['department_count'] = department_count
    #             qs_plan = SaplingPlan.objects.filter(
    #                 department_id=department.id, date__range=[start, end], status=1).aggregate(Sum('count'))
    #             data['year_plan'] = qs_plan['count__sum'] if qs_plan['count__sum'] else 0
    #             actual = tuple()
    #             for item in qs:
    #                 actual += (self.get_actual_by_plants(plant_id=item.id, dep_id=department),)
    #             data['actual'] = actual
    #             all_data_department.append(data)
    #     return all_data_department
    #
    # def get_actual_by_plants(self, plant_id, dep_id):
    #     qs_actual = Sapling.objects.filter(
    #         department_id=dep_id, plant_id=plant_id, date__range=[self._from, self._to], status=1).aggregate(Sum('count'))
    #     return qs_actual['count__sum'] if qs_actual['count__sum'] else 0

    def get_sapling_year_plan(self, dep_id, start, end):
        qs_plan = SaplingPlan.objects.filter(
            department_id=dep_id, date__range=[start, end], status=1).aggregate(Sum('count'))
        return qs_plan['count__sum'] if qs_plan['count__sum'] else 0




