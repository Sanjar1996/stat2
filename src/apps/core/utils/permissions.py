

class AccessPermission:
    """
    permission_model is Required
    To use this Permission class you most add this dictionary in your context data
    """
    permission_required = ''
    permission_denied_object = {}
    permission_denied_key: str = 'permission_denied'

    def get_permissions(self, user=None):
        role = self.get_user_role(user=user)
        if role['is_superuser']:
            return True
        elif role['is_anonymous']:
            return False
        else:
            is_permission = self.get_user_permission(user=user)
            if is_permission is not None:
                return is_permission
            else:
                return False

    @staticmethod
    def get_user_role(user=None):
        if user is not None:
            if user.is_anonymous:
                return dict(is_superuser=False, is_anonymous=True)
            elif user.is_authenticated:
                if user.is_superuser:
                    return dict(is_superuser=True, is_anonymous=False)
                else:
                    return dict(is_superuser=False, is_anonymous=False)
            else:
                raise ValueError('Expected User, but got None')
        else:
            raise ValueError('Expected User, but got None')

    def get_user_permission(self, user=None):
        # print("SELF-permission_required......", self.permission_required)
        # print("Permissions......", user.get_group_permissions())
        for action in user.get_group_permissions():
            # print("Action....", action)
            if action == self.permission_required:
                # print("IF...", action)
                return True
            # else:
            #     return False
