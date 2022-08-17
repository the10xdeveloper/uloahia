from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from ahia.decorators import vendee_required


@method_decorator([login_required, vendee_required], name='dispatch')
class VendeeHomeView(TemplateView):
    template_name = 'vendees/vendee-home.html'
