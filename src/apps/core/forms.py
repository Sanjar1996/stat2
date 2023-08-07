from django import forms

from ..accounts.models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"

            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        ))


class SignUpForm(forms.ModelForm):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                'autofocus': 'autofocus'

            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    mid_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    birth_date = forms.DateField(
        widget=DateInput(
            attrs={
                "class": "form-control",
                "name": "date",
            }
        )
    )
    birth_place = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    citizen_of = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    job_position = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name', 'mid_name', 'birth_date', 'birth_place',
            'citizen_of', 'phone_number', 'job_position', 'password1', 'password2')
