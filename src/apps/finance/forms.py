from .models import FinanceType, Finance, FinancePlan, ProductionServiceActual, ProductionServicePlan
from django import forms
from django.forms import (formset_factory, modelformset_factory)
from ..accounts.models import Department, Region, User
from django.utils.translation import ugettext_lazy as _

AMOUNT_TYPE = (
    (1, _("Xojalik hisobi")),
    (2, _("Xususiy sektor"))
)
STATUS = ((1, _("NEW")), (2, _("CONFIRM")), (3, _("DELETE")))


class DateInput(forms.DateInput):
    input_type = 'date'


class FilterForm(forms.Form):
    start = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    end = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))


AMOUNT_STATUSES = (
    (1, _("Xojalik hisobi")),
    (2, _("Xususiy sektor"))
)


class FinanceFilterForm(forms.Form):
    type = forms.ChoiceField(choices=AMOUNT_STATUSES, widget=forms.Select(
        attrs={"class": "form-control", }), required=False)
    start = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    end = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))


class FinanceTypeForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = FinanceType
        fields = ('name',)


class FinanceForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    amount = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Amount",
                "class": "form-control"
            }
        ))
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(status=1),
        to_field_name='name', empty_label="Select Department"
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.filter(status=1),
        to_field_name='name', empty_label="Select region"
    )
    amount_type = forms.ChoiceField(choices=AMOUNT_TYPE, widget=forms.Select(attrs={"class": "custom-select", }),
                                    required=False)
    type = forms.ModelChoiceField(
        queryset=FinanceType.objects.filter(status=1),
        to_field_name='name', empty_label="Select finance type"
    )
    state = forms.ChoiceField(choices=STATUS, widget=forms.Select(attrs={"class": "custom-select", }),
                              required=False)

    class Meta:
        model = Finance
        fields = ('date', 'amount', 'department', 'region', 'creator', 'type', "amount_type", "state")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['department'].widget.attrs.update({
            'class': 'custom-select',
            'name': 'department',
            'required': 'required',
        })
        self.fields['region'].widget.attrs.update({
            'class': 'custom-select',
            'name': 'region',
            'required': 'required',
        })

        self.fields['type'].widget.attrs.update({
            'class': 'custom-select',
            'required': 'required'
        })
        self.fields['state'].required = False


class ProductionServiceActualForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    production = forms.FloatField(widget=forms.TextInput(attrs={"class": "form-control"}))
    paid_service = forms.FloatField(widget=forms.TextInput(attrs={"class": "form-control"}))
    department = forms.ModelChoiceField(queryset=Department.objects.filter(status=1),
                                        to_field_name='name', empty_label="Select Department"
                                        )
    region = forms.ModelChoiceField(queryset=Region.objects.filter(status=1),
                                    to_field_name='name', empty_label="Select region"
                                    )

    class Meta:
        model = ProductionServiceActual
        fields = ('date', 'production', "paid_service", 'department', 'region')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['department'].widget.attrs.update({
            'class': 'custom-select',
            'name': 'department',
            'required': 'required',
        })
        self.fields['region'].widget.attrs.update({
            'class': 'custom-select',
            'name': 'region',
            'required': 'required',
        })


class ProductionServicePlanForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    production = forms.FloatField(widget=forms.TextInput(attrs={"class": "form-control"}))
    paid_service = forms.FloatField(widget=forms.TextInput(attrs={"class": "form-control"}))
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(status=1),
        to_field_name='name', empty_label="Select Department"
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.filter(status=1),
        to_field_name='name', empty_label="Select region"
    )

    class Meta:
        model = ProductionServicePlan
        fields = ('date', 'production', "paid_service", 'department', 'region')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['department'].widget.attrs.update({
            'class': 'custom-select',
            'name': 'department',
            'required': 'required',
        })
        self.fields['region'].widget.attrs.update({
            'class': 'custom-select',
            'name': 'region',
            'required': 'required',
        })


class FinancePlanForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    amount = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Amount",
                "class": "form-control"
            }
        ))
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(status=1),
        to_field_name='name', empty_label="Select Department"
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.filter(status=1),
        to_field_name='name', empty_label="Select region"
    )

    class Meta:
        model = FinancePlan
        fields = ('date', 'amount', 'department', 'region',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['department'].widget.attrs.update({
            'class': 'form-control',
            'name': 'department',
            'required': 'required',
        })
        self.fields['region'].widget.attrs.update({
            'class': 'form-control',
            'name': 'region',
            'required': 'required',
        })


class FinanceModelForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    amount = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}
    ))
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(status=1), widget=forms.Select(attrs={'class': 'custom-select'}),
        to_field_name='name', empty_label="Select Department")
    region = forms.ModelChoiceField(
        queryset=Region.objects.filter(status=1), widget=forms.Select(attrs={'class': 'custom-select'}),
        to_field_name='name', empty_label="Select Region")
    type = forms.ModelChoiceField(
        queryset=FinanceType.objects.all(), widget=forms.Select(attrs={'class': 'custom-select'}),
        to_field_name='name', empty_label="Select type")

    class Meta:
        model = Finance
        fields = ('date', 'amount', 'department', 'region', 'type')
        labels = {
            'date': 'Date',
            'amount': 'Amount',
            'department': 'Department',
            'region': 'Region',
            'type': 'Finance Type',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['department'].widget.attrs.update({
            'class': 'form-control',
            'name': 'department',
            'required': 'required',
        })
        self.fields['region'].widget.attrs.update({
            'class': 'form-control',
            'name': 'region',
            'required': 'required',
        })
        self.fields['type'].widget.attrs.update({
            'class': 'form-control',
            'required': 'required'
        })


FinanceModelFormSet = formset_factory(FinanceModelForm)


class FinancePlanModelForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    amount = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"}
    ))
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(status=1), widget=forms.Select(attrs={'class': 'custom-select'}),
        to_field_name='name', empty_label="Select Department")
    region = forms.ModelChoiceField(
        queryset=Region.objects.filter(status=1), widget=forms.Select(attrs={'class': 'custom-select'}),
        to_field_name='name', empty_label="Select Region")
    type = forms.ModelChoiceField(
        queryset=FinanceType.objects.filter(status=1), widget=forms.Select(attrs={'class': 'custom-select'}),
        to_field_name='name', empty_label="Select type")

    class Meta:
        model = FinancePlan
        fields = ('date', 'amount', 'department', 'region', 'type')
        labels = {
            'date': 'Date',
            'amount': 'Amount',
            'department': 'Department',
            'region': 'Region',
            'type': 'Finance Type',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['department'].widget.attrs.update({
            'class': 'form-control',
            'name': 'department',
            'required': 'required',
        })
        self.fields['region'].widget.attrs.update({
            'class': 'form-control',
            'name': 'region',
            'required': 'required',
        })
        self.fields['type'].widget.attrs.update({
            'class': 'form-control',
            'required': 'required'
        })


FinancePlanModelFormSet = formset_factory(FinancePlanModelForm)
