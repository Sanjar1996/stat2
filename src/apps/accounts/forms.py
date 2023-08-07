# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..accounts.models import User, UserInformation
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from .models import Region, Department, Position, Nation, Information

USER_STATUSES = ((1, _('new')), (2, _("active")), (3, _("deleted")))
GENDER_TYPES = ((1, _("Male")), (2, _("Female")), (3, "-----"))
CRIPPLE_TYPE = ((1, _("no")), (2, _('yes')))


class DateInput(forms.DateInput):
    input_type = 'date'


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "value": "ApS12_ZZs8",
                "class": "form-control"
            }
        ))


class SignUpForm2(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class SignUpForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "autofocus": "autofocus"}
    ))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}
    ))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}
    ))
    mid_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}))
    temporary_work = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}
    ))
    information = forms.ModelChoiceField(
        queryset=Information.objects.exclude(status=2), widget=forms.Select(
            attrs={'class': 'form-control'}),
        to_field_name='name', empty_label=_("Select Information"))

    position = forms.ModelChoiceField(
        queryset=Position.objects.exclude(status=2), widget=forms.Select(
            attrs={'class': 'form-control'}),
        to_field_name='name', empty_label=_("Select position"))

    national = forms.ModelChoiceField(
        queryset=Nation.objects.exclude(status=2), widget=forms.Select(
            attrs={'class': 'form-control'}),
        to_field_name='name', empty_label=_("Select nation"))

    department = forms.ModelChoiceField(
        queryset=Department.objects.exclude(status=2), widget=forms.Select(
            attrs={'class': 'form-control'}),
        to_field_name='name', empty_label=_("Select department"))
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', }),
    )

    status = forms.ChoiceField(choices=USER_STATUSES, widget=forms.Select(
        attrs={"class": "form-control", }), required=False)

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control"}
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control"}
    ))

    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name',
            'mid_name', 'temporary_work', 'information',
            'position', 'national', 'department', 'groups',
            'status', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['groups'].required = False


class UserUpdateForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "autofocus": "autofocus"}
    ))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}
    ))
    mid_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}))
    temporary_work = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}
    ))
    information = forms.ModelChoiceField(
        queryset=Information.objects.exclude(status=2), widget=forms.Select(
            attrs={'class': 'form-control'}),
        to_field_name='name', empty_label=_("Select Information"))

    position = forms.ModelChoiceField(
        queryset=Position.objects.exclude(status=2), widget=forms.Select(
            attrs={'class': 'form-control'}),
        to_field_name='name', empty_label=_("Select position"))

    national = forms.ModelChoiceField(
        queryset=Nation.objects.exclude(status=2), widget=forms.Select(
            attrs={'class': 'form-control'}),
        to_field_name='name', empty_label=_("Select nation"))

    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(status=1), widget=forms.Select(
            attrs={'class': 'form-control'}),
        to_field_name='name', empty_label=_("Select department"))
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', }),
    )
    status = forms.ChoiceField(choices=USER_STATUSES, widget=forms.Select(
        attrs={"class": "form-control", }), required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    is_active = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'mid_name',
            'temporary_work',
            'information',
            'position',
            'national',
            'department',
            'groups',
            'status',
            "password",
            "is_active"
        )

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].required = False
        self.fields['groups'].required = False
        self.fields['department'].required = False
        self.fields['national'].required = False
        self.fields['information'].required = False
        self.fields['position'].required = False
        self.fields['temporary_work'].required = False
        self.fields['mid_name'].required = False
        self.fields['status'].required = False
        self.fields['is_active'].widget.attrs.update({
            'class': 'form-check',
            'name': 'activate'
        })


class UserInformationForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True), to_field_name='email',
                                  empty_label="Select user",
                                  required=False
                                  )
    year_of_graduation = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    name_of_graduation = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    birth_date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    birth_place = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    specialization = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    passport_number = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    start_position_date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    end_position_date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    gender = forms.ChoiceField(choices=GENDER_TYPES, widget=forms.Select(attrs={"class": "custom-select", }),
                               required=False)
    residence_address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    academic_degree = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    diploma_number = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    tour = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    favorite_party = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    languages = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    family_number = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))
    people_deputy = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    state_award = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    cripple = forms.ChoiceField(choices=CRIPPLE_TYPE, widget=forms.Select(attrs={"class": "custom-select", }),
                                required=False)
    military_service = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    judicial = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    resume = forms.FileField()
    is_judicial = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = UserInformation
        fields = ("user", "year_of_graduation", "name_of_graduation", "birth_date", "birth_place", "specialization",
                  "passport_number", "start_position_date", "end_position_date", "gender", "residence_address",
                  "phone_number", "academic_degree", "diploma_number", "tour", "favorite_party", "languages",
                  "family_number", "people_deputy", "state_award", "cripple",
                  "military_service", "judicial", "resume", "is_judicial")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['resume'].required = False
        self.fields['is_judicial'].required = False
        self.fields['is_judicial'].widget.attrs.update({
            'class': 'form-check',
            'name': 'Judical',
        })
        self.fields['year_of_graduation'].required = False
        self.fields['name_of_graduation'].required = False
        self.fields['birth_date'].required = False
        self.fields['birth_place'].required = False
        self.fields['specialization'].required = False
        self.fields['passport_number'].required = False
        self.fields['start_position_date'].required = False
        self.fields['end_position_date'].required = False
        self.fields['gender'].required = False
        self.fields['residence_address'].required = False
        self.fields['phone_number'].required = False
        self.fields['academic_degree'].required = False
        self.fields['tour'].required = False
        self.fields['favorite_party'].required = False
        self.fields['languages'].required = False
        self.fields['family_number'].required = False
        self.fields['people_deputy'].required = False
        self.fields['state_award'].required = False
        self.fields['cripple'].required = False
        self.fields['military_service'].required = False
        self.fields['judicial'].required = False
        self.fields['resume'].required = False
        self.fields['is_judicial'].required = False
        self.fields['diploma_number'].required = False


class UserCreateForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "autofocus": "autofocus"}
    ))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}
    ))
    mid_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}))
    temporary_work = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}
    ))
    information = forms.ModelChoiceField(
        queryset=Information.objects.exclude(status=2), widget=forms.Select(
            attrs={'class': 'form-control'}),
        to_field_name='name', empty_label=_("Select Information"))

    position = forms.ModelChoiceField(
        queryset=Position.objects.exclude(status=2), widget=forms.Select(
            attrs={'class': 'form-control'}),
        to_field_name='name', empty_label=_("Select position"))

    national = forms.ModelChoiceField(
        queryset=Nation.objects.exclude(status=2), widget=forms.Select(
            attrs={'class': 'form-control'}),
        to_field_name='name', empty_label=_("Select nation"))

    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(status=1), widget=forms.Select(
            attrs={'class': 'form-control'}),
        to_field_name='name', empty_label=_("Select department"))
    # groups = forms.ModelChoiceField(
    #     queryset=Group.objects.all(),
    #     widget=forms.Select(attrs={'class': 'form-control', }),
    # )
    status = forms.ChoiceField(choices=USER_STATUSES, widget=forms.Select(
        attrs={"class": "form-control", }), required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control"}
    ))
    is_active = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'mid_name', 'temporary_work',
                  'information', 'position', 'national', 'department', 'groups', 'password', 'is_active')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['groups'].widget.attrs.update({
            'class': 'custom-select',
            'name': 'groups',
            'required': False,
        })
        self.fields['national'].widget.attrs.update({
            'class': 'custom-select',
            'name': 'national',
            'required': False,
        })
        self.fields['information'].widget.attrs.update({
            'class': 'custom-select',
            'name': 'department',
            'required': False,
        })
        self.fields['position'].widget.attrs.update({
            'class': 'custom-select',
            'name': 'department',
            'required': False,
        })
        self.fields['temporary_work'].required = False
        self.fields['mid_name'].required = False
        self.fields['status'].widget.attrs.update({
            'class': 'custom-select',
            'name': 'status',
            'required': False,
        })
        self.fields['department'].widget.attrs.update({
            'class': 'custom-select',
            'name': 'department',
            'required': False,
        })
        self.fields['is_active'].widget.attrs.update({
            'class': 'form-check',
            'name': 'is_active',
        })


class RegionForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Region
        fields = ('name',)


class PositionForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))

    class Meta:
        model = Position
        fields = ('name',)


class NationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))

    class Meta:
        model = Nation
        fields = ('name',)


class InformationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))

    class Meta:
        model = Information
        fields = ('name',)


class DepartmentForm(forms.ModelForm):
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        to_field_name='name', empty_label="----------",

    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))

    class Meta:
        model = Department
        fields = ('region', 'name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['region'].widget.attrs.update({
            'class': 'custom-select',
            'name': 'region',
            'required': 'required',
        })


class FilterForm(forms.Form):
    start = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    end = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
