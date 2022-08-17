from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, DetailView

from ahia.decorators import vendor_required
from vendors.forms import WebUserUpdateForm, VendorUpdateForm


@method_decorator([login_required, vendor_required], name='dispatch')
class VendorsHomeView(TemplateView):
    template_name = 'vendors/vendor-home.html'
    pass


class VendorCatalogHomeView(TemplateView):
    template_name = 'vendors/vendor-catalog.html'
    pass


class VendorUpdateView(FormView):
    def get(self, request, *args, **kwargs):
        web_user_form = WebUserUpdateForm(instance=request.user)
        vendor_form = VendorUpdateForm(instance=request.user.vendor)
        context = {
            'web_user_form': web_user_form,
            'vendor_form': vendor_form
        }
        return render(request, 'vendors/vendor-edit-profile.html', context)

    def post(self, request, *args, **kwargs):
        web_user_form = WebUserUpdateForm(request.POST, request.FILES, instance=request.user)
        vendor_form = VendorUpdateForm(request.POST, instance=request.user.vendor)

        if web_user_form.is_valid() and vendor_form.is_valid():
            web_user_form.save()
            vendor_form.save()
            messages.success(request, f" Your vendor account has been updated successfully!")
            update_session_auth_hash(request, request.user)
            return redirect('vendors:vendors-home')


class VendorDetailView(DetailView):
    template_name = ''

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'vendor'
        return super().get_context_data(**kwargs)

    def get_object(self, queryset=None):
        return self.request.user
