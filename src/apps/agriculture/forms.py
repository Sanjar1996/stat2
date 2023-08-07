from django import forms

from .models import AgricultureActual, AgriculturePlan
from ..accounts.models import Department, Region
from ..trees.models import TreePlant, TreeTypes


class DateInput(forms.DateInput):
    input_type = 'date'


class AgricultureActualForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    hectare = forms.FloatField(widget=forms.TextInput(attrs={"placeholder": "hectare", "class": "form-control"}))
    weight = forms.FloatField(widget=forms.TextInput(attrs={"placeholder": "weight(tonna)", "class": "form-control"}))
    department = forms.ModelChoiceField(queryset=Department.objects.filter(status=1), to_field_name='name',
                                        empty_label="Select Department")
    profit = forms.FloatField(widget=forms.NumberInput(attrs={"class": "form-control"}))
    yield_area = forms.FloatField(widget=forms.NumberInput(attrs={"class": "form-control"}))
    region = forms.ModelChoiceField(queryset=Region.objects.filter(status=1), to_field_name='name',
                                    empty_label="Select region")
    tree_plant = forms.ModelChoiceField(queryset=TreePlant.objects.filter(status=1), to_field_name='name',
                                        empty_label="Select tree plant")
    tree_type = forms.ModelChoiceField(queryset=TreeTypes.objects.filter(status=1))
    show_yield_area = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = AgricultureActual
        fields = ('date', 'hectare', "weight", 'department', 'region', 'creator', 'tree_plant',
                  "tree_type", "tree_type", "show_yield_area",
                  "profit", "yield_area")

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
        self.fields['tree_plant'].widget.attrs.update({
            'class': 'custom-select',
            'required': 'required'
        })
        self.fields['tree_type'].widget.attrs.update({
            'class': 'custom-select',
            'required': 'required'
        })
        self.fields['tree_type'].widget.attrs.update({
            'class': 'custom-select',
            'required': 'required'
        })
        self.fields['show_yield_area'].widget.attrs.update({
            'class': 'form-check',
        })
        self.fields['profit'].required = False
        self.fields['yield_area'].required = False


class AgriculturePlanForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    hectare = forms.FloatField(widget=forms.TextInput(attrs={"placeholder": "hectare", "class": "form-control"}))

    weight = forms.FloatField(widget=forms.TextInput(attrs={"placeholder": "weight(tonna)", "class": "form-control"}))
    department = forms.ModelChoiceField(queryset=Department.objects.filter(status=1), to_field_name='name',
                                        empty_label="---------"
                                        )
    region = forms.ModelChoiceField(queryset=Region.objects.filter(status=1), to_field_name='name',
                                    empty_label="----------")
    # tree_plant = forms.ModelChoiceField(queryset=TreePlant.objects.filter(status=1), to_field_name='name',
    #                                     empty_label="---------")
    tree_plant = forms.ModelChoiceField(queryset=TreePlant.objects.filter(status=1), to_field_name='name',
                                        empty_label="---------")
    tree_type = forms.ModelChoiceField(queryset=TreeTypes.objects.filter(status=1), to_field_name='name',
                                       empty_label="---------")

    class Meta:
        model = AgriculturePlan
        fields = ('date', 'hectare', "weight", 'department', 'region',
                  'creator', 'tree_plant', 'tree_type')

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
        self.fields['tree_plant'].widget.attrs.update({
            'class': 'custom-select',
            'required': 'required'
        })
        self.fields['tree_type'].widget.attrs.update({
            'class': 'custom-select',
            "name": "tree_type",
            'required': 'required'
        })

