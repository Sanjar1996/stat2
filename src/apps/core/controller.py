import calendar
import datetime

from django.core.serializers import serialize
from django.db.models import Sum
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .service import get_current_user_regions_and_departments_qs, get_production_and_paid_service_data
from .utils.permissions import *


class RouteController(LoginRequiredMixin, View):
    """Base URL: http://127.0.0.1:8000"""
    html_template = loader.get_template('index.html')

    def get(self, request):
        if request.user.is_authenticated:
            context = get_production_and_paid_service_data(request.user)
            return HttpResponse(self.html_template.render(context, request))
        else:
            return redirect('controller:login')


class LoginView(View):
    """http://127.0.0.1:8000/login"""
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        else:
            pass
        form = LoginForm()
        context = {'form': form, 'msg': ''}
        return render(request, self.template_name, context)

    def post(self, request):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
        return render(request, self.template_name, {"form": form, "msg": msg})


class RegisterUserView(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/register"""
    template_name = 'accounts/register.html'

    def get(self, request):
        form = SignUpForm()
        context = {'form': form, 'msg': ''}
        return render(request, self.template_name, context)

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            raw_password = form.cleaned_data.get('password1')
            # email = form.cleaned_data.get("email")
            saved_user = form.save(commit=False)
            saved_user.set_password(raw_password)
            saved_user.save()
            # user = authenticate(email=email, password=raw_password)
            # if user is not None:
            #     login(request, user)
            #     return redirect("/")
            return redirect("/")
            # else:
            #     msg = 'Invalid credentials'
        else:
            msg = form.errors
        return render(request, self.template_name, {"form": form, "msg": msg})


class LogoutView(View):
    """http://127.0.0.1:8000/logout"""

    def get(self, request):
        logout(request)
        return redirect('controller:login')













