from django import forms
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resources import GroupsResource
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse_lazy
from . import models


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.User
        fields = ('email', 'password', 'is_active', 'is_superuser')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = ("<a href=\"%s\"><strong>Change Password</strong></a>"
                                             ) % reverse_lazy('admin:auth_user_password_change', args=[self.instance.id])

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'role', 'status', 'position', 'is_staff',  'is_superuser')
    list_filter = ('department__region__name', 'groups', 'is_staff', 'is_superuser',)

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'mid_name', 'information', 'position',
                           'temporary_work', 'national',  'department','password',
                           'status', 'is_active', 'is_staff',)}),
        ('Personal info', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'mid_name', 'information', 'position',
                           'temporary_work', 'national', 'groups', 'department',
                           'password1', 'password2',
                           'status', 'is_active', 'is_staff')}),
    )
    search_fields = ('email', 'first_name', 'last_name', 'mid_name', )
    ordering = ('email',)
    filter_horizontal = ('user_permissions',)


class UserInformationAdmin(admin.ModelAdmin):
    list_display = ('user', "year_of_graduation","name_of_graduation","birth_date","birth_place","specialization","passport_number",
                    "start_position_date", "end_position_date","gender","residence_address","phone_number"
                    ,"academic_degree", "diploma_number", "tour","favorite_party","languages","family_number",
                    "people_deputy","state_award","cripple","military_service", "judicial", "is_judicial")
    search_fields = ('user__email',)
    list_display_links = ('user',)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sort', 'status', )
    list_display_links = ('name',)
    search_fields = ['name']


class NationAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    list_display_links = ('name',)
    search_fields = ['name']


class PositionAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'status')
    list_display_links = ('name',)
    search_fields = ['name']


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'region_id', 'region', 'sort', 'status')
    list_display_links = ('name',)
    list_filter = ('region', 'sort',)
    search_fields = ['name']


class InformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    list_display_links = ('name',)
    search_fields = ['name']


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'codename')

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return False


class UserDepartmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_id', 'region', 'department')
    list_filter = ('regions', )
    search_fields = ('user__email', 'regions__name', 'departments__name')


class CustomRoleAdmin(GroupAdmin, ImportExportModelAdmin):
    resource_class = GroupsResource


admin.site.register(Permission, PermissionAdmin)
admin.site.register(models.Region, RegionAdmin)
admin.site.register(models.Nation, NationAdmin)
admin.site.register(models.Position, PositionAdmin)
admin.site.register(models.Department, DepartmentAdmin)
admin.site.register(models.Information, InformationAdmin)
admin.site.register(models.UserInformation, UserInformationAdmin)

admin.site.register(models.User, UserAdmin)
admin.site.register(models.UserDepartment, UserDepartmentAdmin)
admin.site.unregister(Group)
admin.site.register(Group, CustomRoleAdmin)
