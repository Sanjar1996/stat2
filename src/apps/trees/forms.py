from django import forms

from .models import *
from ..accounts.models import Department, Region


class DateInput(forms.DateInput):
    input_type = 'date'


class TreeCategoryForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))

    class Meta:
        model = TreeCategory
        fields = ('name',)


class TreeTypeForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    show_profit = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = TreeTypes
        fields = ('name', "show_profit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['show_profit'].widget.attrs.update({
            'class': 'form-check',
        })


class TreePlantForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=TreeCategory.objects.exclude(status=2),
        to_field_name='name', empty_label="---------"
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    is_show_sprouting = forms.BooleanField(required=False)
    is_show_seed = forms.BooleanField(required=False)
    is_show_sapling = forms.BooleanField(required=False)
    is_show_height = forms.BooleanField(required=False)

    class Meta:
        model = TreePlant
        fields = (
            'name', 'description', 'category', "is_show_sprouting", "is_show_seed", "is_show_sapling",
            "is_show_height",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['category'].widget.attrs.update({
            'class': 'custom-select',
            'name': 'name',
            'required': False,
        })
        self.fields['category'].required = False
        self.fields['is_show_sprouting'].widget.attrs.update({
            'class': 'form-check'
        })
        self.fields['is_show_seed'].widget.attrs.update({
            'class': 'form-check'
        })
        self.fields['is_show_sapling'].widget.attrs.update({
            'class': 'form-check'
        })
        self.fields['is_show_height'].widget.attrs.update({
            'class': 'form-check'
        })


class TreeHeightForm(forms.ModelForm):
    tree_plan = forms.ModelChoiceField(
        queryset=TreePlant.objects.filter(is_show_height=True, status=1),
        to_field_name='name', empty_label="--------"
    )
    height_0_0_2_count = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "0,2 м гача",
                "class": "form-control"
            }
        ))
    height_0_2_5_count = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "0,2 дан 0,5 м гача",
                "class": "form-control"
            }
        ))
    height_0_5_1_count = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "0,5 -1 м. гача",
                "class": "form-control"
            }
        ))
    height_1_1_5_count = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "1-1,5 м гача",
                "class": "form-control"
            }
        ))
    height_1_5_2_count = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "1,5-2 м гача",
                "class": "form-control"
            }
        ))
    date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    region = forms.ModelChoiceField(
        queryset=Region.objects.filter(status=1),
        to_field_name='name', empty_label="--------"
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(status=1),
        to_field_name='name', empty_label="---------"
    )

    class Meta:
        model = TreeHeightReport
        fields = ("tree_plan",
                  "height_0_0_2_count",
                  "height_0_2_5_count",
                  "height_0_5_1_count",
                  "height_1_1_5_count",
                  "height_1_5_2_count",
                  "date",
                  "region",
                  "department")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['height_0_0_2_count'].required = False
        self.fields['height_0_2_5_count'].required = False
        self.fields['height_0_5_1_count'].required = False
        self.fields['height_1_1_5_count'].required = False
        self.fields['height_1_5_2_count'].required = False
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
        self.fields['tree_plan'].widget.attrs.update({
            'class': 'form-control',
            "name": 'tree_plant',
            'required': 'required'
        })


class TreeContractForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=TreeContractCategory.objects.filter(status=1),
        to_field_name='name', empty_label="--------"
    )
    count = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        ))
    amount = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        ))
    payout = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        ))
    output_tree = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        ))
    date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    region = forms.ModelChoiceField(
        queryset=Region.objects.filter(status=1),
        to_field_name='name', empty_label="--------"
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(status=1),
        to_field_name='name', empty_label="---------"
    )

    class Meta:
        model = TreeContract
        fields = ("category",
                  "count",
                  "amount",
                  "payout",
                  "output_tree",
                  "date",
                  "region",
                  "department")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['count'].required = False
        self.fields['amount'].required = False
        self.fields['payout'].required = False
        self.fields['output_tree'].required = False
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
        self.fields['category'].widget.attrs.update({
            'class': 'form-control',
            "name": 'category',
            'required': 'required'
        })


class TreeContractPlanForm(forms.ModelForm):
    tree_count = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        ))
    region = forms.ModelChoiceField(
        queryset=Region.objects.filter(status=1),
        to_field_name='name', empty_label="--------"
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(status=1),
        to_field_name='name', empty_label="---------"
    )

    class Meta:
        model = TreeContractPlan
        fields = ("tree_count",
                  "region",
                  "department")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tree_count'].required = True
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


class SaplingForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    count = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Amount",
                "class": "form-control",
                "step": "0.01",
                "min": "0.00"
            }
        ))
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(status=1),
        to_field_name='name', empty_label="------------"
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.filter(status=1),
        to_field_name='name', empty_label="------------"
    )
    plant = forms.ModelChoiceField(
        queryset=TreePlant.objects.filter(status=1, is_show_sprouting=True),
        to_field_name='name', empty_label="-------------"
    )

    class Meta:
        model = Sapling
        fields = ('date', 'count', 'department', 'region', 'creator', 'plant')

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
        self.fields['plant'].widget.attrs.update({
            'class': 'custom-select',
            'required': 'required'
        })


class SaplingPlanForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    count = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Amount",
                "class": "form-control",
                "step": "0.01",
                "min": "0.00"
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

    # creator = forms.ModelChoiceField(
    #     queryset=User.objects.filter(is_active=True),
    #     to_field_name='first_name',
    #     empty_label="Select user",
    #     required=False
    # )
    class Meta:
        model = SaplingPlan
        fields = ('date', 'count', 'department', 'region', 'creator',)

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
        # self.fields['creator'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': 'creator',
        # })


# SEED
class SeedForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    count = forms.FloatField(
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
    # creator = forms.ModelChoiceField(
    #     queryset=User.objects.filter(is_active=True),
    #     to_field_name='first_name',
    #     empty_label="Select user",
    #     required=False
    # )
    plant = forms.ModelChoiceField(
        queryset=TreePlant.objects.filter(status=1, is_show_seed=True),
        to_field_name='name', empty_label="Select tree plant"
    )

    class Meta:
        model = Seed
        fields = ('date', 'count', 'department', 'region', 'creator', 'plant')

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
        # self.fields['creator'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': 'creator',
        # })
        self.fields['plant'].widget.attrs.update({
            'class': 'custom-select',
            'required': 'required'
        })


class SeedPlanForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    count = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Count",
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
    # creator = forms.ModelChoiceField(
    #     queryset=User.objects.filter(is_active=True),
    #     to_field_name='first_name',
    #     empty_label="Select user",
    #     required=False
    # )
    plant = forms.ModelChoiceField(
        queryset=TreePlant.objects.filter(is_show_seed=True, status=1),
        to_field_name='name', empty_label="Select tree plant"
    )

    class Meta:
        model = SeedPlan
        fields = ('date', 'count', 'department', 'region', 'creator', 'plant',)

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
        # self.fields['creator'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': 'creator',
        # })
        self.fields['plant'].widget.attrs.update({
            'class': 'form-control',
            'required': 'required'
        })


# SPROUTS

class SproutForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    count = forms.FloatField(
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

    plant = forms.ModelChoiceField(
        queryset=TreePlant.objects.filter(status=1, is_show_sprouting=True),
        to_field_name='name', empty_label="Select tree plant"
    )

    class Meta:
        model = Sprout
        fields = ('date', 'count', 'department', 'region', 'creator', 'plant')

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
        self.fields['plant'].widget.attrs.update({
            'class': 'custom-select',
            'required': 'required'
        })


class SproutPlanForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    count = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Count",
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
    # creator = forms.ModelChoiceField(
    #     queryset=User.objects.filter(is_active=True),
    #     to_field_name='first_name',
    #     empty_label="Select user",
    #     required=False
    # )
    plant = forms.ModelChoiceField(
        queryset=TreePlant.objects.filter(is_show_sprouting=True, status=1),
        to_field_name='name', empty_label="Select tree plant"
    )

    class Meta:
        model = SproutPlan
        fields = ('date', 'count', 'department', 'region', 'creator', 'plant',)

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
        # self.fields['creator'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': 'creator',
        # })
        self.fields['plant'].widget.attrs.update({
            'class': 'form-control',
            'required': 'required'
        })


class SproutInputForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    donation = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "donation",
                "class": "form-control"
            }
        ))
    buying = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "buying",
                "class": "form-control"
            }
        ))
    new_sprout = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "new_sprout",
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
    # creator = forms.ModelChoiceField(
    #     queryset=User.objects.filter(is_active=True),
    #     to_field_name='first_name',
    #     empty_label="Select user",
    #     required=False
    # )
    plant = forms.ModelChoiceField(
        queryset=TreePlant.objects.filter(is_show_sprouting=True, status=1),
        to_field_name='name', empty_label="Select tree plant"
    )
    category = forms.ModelChoiceField(
        queryset=TreeCategory.objects.filter(status=1),
        to_field_name='name', empty_label="Select tree category"
    )

    class Meta:
        model = SproutInput
        fields = ('date', 'donation', 'buying', "new_sprout", 'department', 'region', 'creator', 'plant', 'category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
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
        # self.fields['creator'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': 'creator',
        # })
        self.fields['plant'].widget.attrs.update({
            'class': 'form-control',
            'required': 'required'
        })


class SproutOutputForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    donation = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "donation",
                "class": "form-control"
            }
        ))
    selling = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "selling",
                "class": "form-control"
            }
        ))
    for_the_forest = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "for the forest",
                "class": "form-control"
            }
        ))
    place_changed = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "place changed",
                "class": "form-control"
            }
        ))
    unsuccessful = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "unsuccessful",
                "class": "form-control"
            }
        ))
    out_of_count = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Xisobdan chiqarilgan",
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
    plant = forms.ModelChoiceField(
        queryset=TreePlant.objects.filter(is_show_sprouting=True, status=1),
        to_field_name='name', empty_label="Select tree plant"
    )
    category = forms.ModelChoiceField(
        queryset=TreeCategory.objects.filter(status=1),
        to_field_name='name', empty_label="Select tree category"
    )

    class Meta:
        model = SproutOutput
        fields = ('date', 'donation', 'selling', "for_the_forest", "unsuccessful", 'department', "place_changed",
                  "out_of_count", 'region', 'creator', 'plant', 'category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
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
        # self.fields['creator'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': 'creator',
        # })
        self.fields['plant'].widget.attrs.update({
            'class': 'form-control',
            'required': 'required'
        })


class SaplingInputForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    donation = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "donation",
                "class": "form-control"
            }
        ))
    buying = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "buying",
                "class": "form-control"
            }
        ))
    new_sprout = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "new_sprout",
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
    plant = forms.ModelChoiceField(
        queryset=TreePlant.objects.filter(is_show_sprouting=True, status=1),
        to_field_name='name', empty_label="Select tree plant"
    )
    category = forms.ModelChoiceField(
        queryset=TreeCategory.objects.filter(status=1),
        to_field_name='name', empty_label="Select tree category"
    )

    class Meta:
        model = SaplingInput
        fields = ('date', 'donation', 'buying', "new_sprout", 'department', 'region', 'creator', 'plant', 'category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
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
        self.fields['plant'].widget.attrs.update({
            'class': 'form-control',
            'required': 'required'
        })


class SaplingOutputForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    donation = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "donation",
                "class": "form-control"
            }
        ))
    selling = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "selling",
                "class": "form-control"
            }
        ))
    for_the_forest = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "for the forest",
                "class": "form-control"
            }
        ))
    place_changed = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "place changed",
                "class": "form-control"
            }
        ))
    unsuccessful = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "unsuccessful",
                "class": "form-control"
            }
        ))
    out_of_count = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Xisobdan chiqarilgan",
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
    plant = forms.ModelChoiceField(
        queryset=TreePlant.objects.filter(is_show_sprouting=True, status=1),
        to_field_name='name', empty_label="Select tree plant"
    )
    category = forms.ModelChoiceField(
        queryset=TreeCategory.objects.filter(status=1),
        to_field_name='name', empty_label="Select tree category"
    )

    class Meta:
        model = SaplingOutput
        fields = ('date', 'donation', 'selling', "for_the_forest", "unsuccessful", 'department', "place_changed",
                  "out_of_count", 'region', 'creator', 'plant', 'category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
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
        # self.fields['creator'].widget.attrs.update({
        #     'class': 'form-control',
        #     'name': 'creator',
        # })
        self.fields['plant'].widget.attrs.update({
            'class': 'form-control',
            'required': 'required'
        })


# PREPAIRLAND LandPlanForm
class LandForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    hectare = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Hectare",
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
    categories = forms.ModelChoiceField(
        queryset=LandCategory.objects.exclude(status=2),
        to_field_name='name', empty_label="Select category"
    )

    class Meta:
        model = PrepairLand
        fields = ('date', 'hectare', 'department', 'region', 'categories')

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
        self.fields['categories'].widget.attrs.update({
            'class': 'custom-select',
            'required': 'required'
        })


# THE GROUND PLANTING
class TheGroundPlantingForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(status=1),
        to_field_name='name', empty_label="Select Department"
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.filter(status=1),
        to_field_name='name', empty_label="Select region"
    )

    class Meta:
        model = TreeGroundPlanting
        fields = (
            'date', "desert_plant", "walnut", "pistachios", "nut", "poplar", "paulownia", "other_plants", 'department',
            'region')

        widgets = {
            "desert_plant": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.00"}),
            "walnut": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.00"}),
            "pistachios": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.00"}),
            "nut": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.00"}),
            "poplar": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.00"}),
            "paulownia": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.00"}),
            "other_plants": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.00"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['desert_plant'].required = False
        self.fields['walnut'].required = False
        self.fields['pistachios'].required = False
        self.fields['nut'].required = False
        self.fields['poplar'].required = False
        self.fields['paulownia'].required = False
        self.fields['other_plants'].required = False
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


class TheGroundPlantingPlanForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control"
    }))
    # desert_plant = forms.FloatField(widget=forms.TextInput(attrs={"class": "form-control"}))
    # walnut = forms.FloatField(widget=forms.TextInput(attrs={"class": "form-control"}))
    # pistachios = forms.FloatField(widget=forms.TextInput(attrs={"class": "form-control"}))
    # nut = forms.FloatField(widget=forms.TextInput(attrs={"class": "form-control"}))
    # poplar = forms.FloatField(widget=forms.TextInput(attrs={"class": "form-control"}))
    # paulownia = forms.FloatField(widget=forms.TextInput(attrs={"class": "form-control"}))
    # other_plants = forms.FloatField(widget=forms.TextInput(attrs={"class": "form-control"}))
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(status=1),
        to_field_name='name', empty_label="Select Department"
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.filter(status=1),
        to_field_name='name', empty_label="Select region"
    )

    class Meta:
        model = TreeGroundPlantingPlan
        fields = (
            'date', "desert_plant", "walnut", "pistachios", "nut", "poplar", "paulownia", "other_plants", 'department',
            'region')
        widgets = {
            "desert_plant": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.00"}),
            "walnut": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.00"}),
            "pistachios": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.00"}),
            "nut": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.00"}),
            "poplar": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.00"}),
            "paulownia": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.00"}),
            "other_plants": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.00"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['desert_plant'].required = False
        self.fields['walnut'].required = False
        self.fields['pistachios'].required = False
        self.fields['nut'].required = False
        self.fields['poplar'].required = False
        self.fields['paulownia'].required = False
        self.fields['other_plants'].required = False
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
