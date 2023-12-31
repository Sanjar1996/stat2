from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class PnflActionListView(LoginRequiredMixin, View):
    template_name = 'accounts/get_pnfl_list.html'

    def get(self, request):
        return render(request, self.template_name)
