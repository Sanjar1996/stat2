from import_export import resources
from django.contrib.auth.models import Group


class GroupsResource(resources.ModelResource):
    class Meta:
        model = Group
        skip_unchanged = True
        report_skipped = True
        fields = ('id', 'name', 'permissions')
