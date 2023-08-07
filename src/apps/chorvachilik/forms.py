from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import *
from ..accounts.models import Department, Region


class DateInput(forms.DateInput):
    input_type = 'date'


class AnimalForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Animal
        fields = ('name',)


class ChorvachilikTypesForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = ChorvachilikTypes
        fields = ('name',)


class ChorvachilikForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    type = forms.ModelMultipleChoiceField(queryset=ChorvachilikTypes.objects.all(), to_field_name='name')
    show_yield_area = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Chorvachilik
        fields = ("name", "type", "show_yield_area")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['type'].widget.attrs.update({
            'class': 'custom-select',
            'name': 'type',
        })


class OutputCategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = ChorvaInputOutputCategory
        fields = ('name',)


class AnimalCategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = AnimalCategory
        fields = ('name',)


class ChorvachilikFilterForm(forms.Form):
    start = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    end = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    type = forms.ModelChoiceField(queryset=ChorvachilikTypes.objects.filter(status=1),
                                  to_field_name='name', empty_label="-------")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['type'].widget.attrs.update({
            'class': 'custom-select',
            'name': 'type',
            'id': 'types',
        })


class ChorvaInOutFilterForm(forms.Form):
    start = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    end = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    category = forms.ModelChoiceField(queryset=AnimalCategory.objects.filter(status=1),
                                      to_field_name='name', empty_label="-------")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].widget.attrs.update({
            'class': 'custom-select',
            'name': 'category',
            "required": False
        })


AMOUNT_TYPES = ((1, _("DONA")), (2, _("KG")), (3, _("HEAD")), (4, _("TON")), (5, _("FAMILY")),)


class ChorvachilikActualForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    amount = forms.FloatField(widget=forms.TextInput(attrs={"placeholder": "amount", "class": "form-control"}))
    department = forms.ModelChoiceField(queryset=Department.objects.filter(status=1), to_field_name='name',
                                        empty_label="---------")
    region = forms.ModelChoiceField(queryset=Region.objects.filter(status=1), to_field_name='name',
                                    empty_label="---------")
    chorvachilik = forms.ModelChoiceField(queryset=Chorvachilik.objects.filter(status=1), to_field_name='name',
                                          empty_label="--------")
    chorvachilik_type = forms.ModelChoiceField(queryset=ChorvachilikTypes.objects.filter(status=1),
                                               to_field_name='name', empty_label="----------")
    amount_type = forms.ChoiceField(choices=AMOUNT_TYPES, widget=forms.Select(attrs={"class": "custom-select", }),
                                    required=False)

    class Meta:
        model = ChorvachilikActual
        fields = ('date', 'amount', "department", 'region', 'chorvachilik', 'chorvachilik_type', 'amount_type',)

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
        self.fields['chorvachilik'].widget.attrs.update({
            'class': 'custom-select',
            'required': 'required'
        })
        self.fields['chorvachilik_type'].widget.attrs.update({
            'class': 'custom-select',
            'required': 'required'
        })


INPUT_OUTPUT_TYPES = ((1, _("KIRIM")), (2, _("CHIQIM")))
STATUS = ((1, _("NEW")), (2, _("CONFIRM")), (2, _("DELETE")))


class InputOutputForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    category = forms.ModelChoiceField(queryset=ChorvaInputOutputCategory.objects.filter(status=1, type=2),
                                      to_field_name='name',
                                      empty_label="------")
    amount = forms.IntegerField(widget=forms.TextInput(attrs={"class": "form-control"}))
    weight = forms.FloatField(widget=forms.TextInput(attrs={"class": "form-control"}))
    type = forms.ChoiceField(choices=INPUT_OUTPUT_TYPES, widget=forms.Select(attrs={"class": "custom-select", }),
                             required=False)
    animal = forms.ModelChoiceField(queryset=Animal.objects.filter(status=1), to_field_name='name',
                                    empty_label="------")
    department = forms.ModelChoiceField(queryset=Department.objects.filter(status=1), to_field_name='name',
                                        empty_label="---------")
    region = forms.ModelChoiceField(queryset=Region.objects.filter(status=1), to_field_name='name',
                                    empty_label="---------")
    status = forms.ChoiceField(choices=STATUS, widget=forms.Select(attrs={"class": "custom-select", }), required=False)

    class Meta:
        model = ChorvaInputOutput
        fields = ['date', "category", "amount", "weight", "type", "animal", "department", "region", "status", "creator"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creator'].required = False
        self.fields['status'].required = False
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
        self.fields['category'].widget.attrs.update({
            'class': 'custom-select',
            'required': 'required'
        })
        self.fields['animal'].widget.attrs.update({
            'class': 'custom-select',
            'required': 'required'
        })
        self.fields['status'].widget.attrs.update({
            'class': 'custom-select',
            'required': False
        })
        self.fields['type'].widget.attrs.update({
            'class': 'custom-select',
            'required': False
        })


class InputOutputFullForm(InputOutputForm):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta(InputOutputForm.Meta):
        fields = InputOutputForm.Meta.fields + ['files']


class UploadFileForm(forms.ModelForm):
    # files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    files = forms.FileField()

    class Meta:
        model = UploadFile
        fields = ['file',]