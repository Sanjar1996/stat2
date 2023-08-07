import django_filters
from django.contrib.postgres.search import SearchVector
from .models import User, Department, Region, Information, Position, Nation

USER_STATUSES = (
    (1, 'Yangi'),
    (2, 'Eski'),
    (3, 'Bekorchi')
)


class MemberFilter(django_filters.FilterSet):
    department__region = django_filters.filters.ModelChoiceFilter(queryset=Region.objects.all())
    department = django_filters.filters.ModelChoiceFilter(queryset=Department.objects.all())
    information = django_filters.filters.ModelChoiceFilter(queryset=Information.objects.all())
    position = django_filters.filters.ModelChoiceFilter(queryset=Position.objects.all())
    national = django_filters.filters.ModelChoiceFilter(queryset=Nation.objects.all())

    email = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(method='search')
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', "department",
                  "department__region", "information", "position", 'national', "is_active"]

    def search(self, queryset, first_name, value):
        return queryset.annotate(search=SearchVector('email', 'last_name', 'first_name'), ).filter(
            search__icontains=value)


# class MemberFilter(django_filters.FilterSet):
#     department__region = django_filters.filters.ModelChoiceFilter(queryset=Region.objects.all())
#     department = django_filters.filters.ModelChoiceFilter(queryset=Department.objects.all())
#     information = django_filters.filters.ModelChoiceFilter(queryset=Information.objects.all())
#     position = django_filters.filters.ModelChoiceFilter(queryset=Position.objects.all())
#     national = django_filters.filters.ModelChoiceFilter(queryset=Nation.objects.all())
#     first_name = django_filters.CharFilter(lookup_expr='icontains')
#     email = django_filters.CharFilter(lookup_expr='icontains')
#     last_name = django_filters.CharFilter(lookup_expr='icontains')
#
#     class Meta:
#         model = User
#         fields = ['email', 'first_name', 'last_name', "department",
#                   "department__region", "information", "position", 'national']

# Agar boolean fild ishlatilsa null ga xam ishlashi uchun
# is_active =  django_filters.BooleanFilter(field_name='department', lookup_expr='isnull')
# wxclude ishlatsaxam boladi
# has_category = django_filters.BooleanFilter(field_name='category', lookup_expr='isnull', exclude=True)
# department__region = django_filters.filters.ModelChoiceFilter(field_name='department__region',
#                                                                   lookup_expr='isnull',
#                                                                   null_label='Uncategorized',
#                                                                   queryset=Region.objects.all())
#     department = django_filters.filters.ModelChoiceFilter(field_name='department',
#                                                           lookup_expr='isnull',
#                                                           null_label='select',queryset=Department.objects.all())
