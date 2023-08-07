from ..models import User, Department,  UserDepartment


class ManagerM2M:

    def save_m2m(self, user_pk, reg, dep):
        user = User.objects.get(pk=user_pk)
        region_list = self.get_list(data=reg)
        department_list = self.get_list(data=dep)
        # print('Region...', len(region_list), 'Department...', len(department_list))
        data = self.remove_invalid_index(departments=department_list, regions=region_list)
        region = data['reg']
        department = self.get_list(data=dep)
        if region and department:
            # print('IF-save_m2m...', 'Region...', len(region), 'Department...', len(department))
            qs_user_department = UserDepartment.objects.filter(user=user)
            if qs_user_department.exists():
                old_user_dep = UserDepartment.objects.get(user=user)
                old_user_dep.regions.clear()
                old_user_dep.departments.clear()
                for reg_item in region:
                    old_user_dep.regions.add(reg_item)
                for dep_item in department:
                    old_user_dep.departments.add(dep_item)
                return old_user_dep
            else:
                new_user_dep = UserDepartment(user=user)
                new_user_dep.save()
                for reg_item in region:
                    new_user_dep.regions.add(reg_item)
                for dep_item in department:
                    new_user_dep.departments.add(dep_item)
                return new_user_dep
        else:
            # print('ELSE-save_m2m.......')
            return False

    def save_user_perms(self, user_pk, perms):
        user = User.objects.get(pk=user_pk)
        permissions = self.get_list(data=perms)
        if permissions:
            if user.groups.exists():
                user.groups.clear()
                for item in permissions:
                    user.groups.add(item)
                return user
            else:
                print('IF-save_user_perms.......', permissions)
                for item in permissions:
                    user.groups.add(item)
                return user
        else:
            print('ELSE-save_user_perms.......')
            return False

    def get_list(self, data):
        valid_list = []
        for item in data:
            valid_list.append(int(item))
        return valid_list

    def remove_invalid_index(self, departments, regions):
        """removing an empty region or an empty department"""
        active_region = []
        active_department = []
        for d_index in departments:
            obj = Department.objects.get(pk=d_index)
            for r_index in regions:
                if obj.region.pk == r_index and r_index not in active_region:
                    active_region.append(r_index)

        # for d_item in departments:
        #     obj = Department.objects.get(pk=d_item)
        #     for a_item in active_region:
        #         if obj.region.pk == a_item and a_item not in active_department:
        #             active_department.append(obj.pk)
        return dict(reg=active_region)
