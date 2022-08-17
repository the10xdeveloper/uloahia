from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView, CreateView

from accounts.forms import LoginForm, VendeeSignUpForm, VendorSignUpForm, ResetPasswordForm

User = get_user_model()


# Account authentication views


# View for logging in members

class LoginView(FormView):
    content = {'form': LoginForm}

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        content = {}
        if request.user.is_authenticated and request.user.is_vendor:
            return redirect(reverse('vendors:vendors-home'))
        elif request.user.is_authenticated and request.user.is_vendee:
            return redirect(reverse('vendee:vendee-home'))
        else:
            pass

        content['form'] = LoginForm
        return render(request, 'authentication/login.html', content)

    def post(self, request, *args, **kwargs):
        content = {}
        email = request.POST['email']
        password = request.POST['password']

        try:
            users = User.objects.filter(email=email)
            user = authenticate(request, email=users.first().email, password=password)
            login(request, user)
            if request.user.is_vendee:
                return redirect(reverse('vendee:vendee-home'))
            elif request.user.is_vendor:
                return redirect(reverse('vendors:vendor-home'))
            else:
                pass

        except Exception as e:
            content = {'form': LoginForm, 'error': 'Unable to login with the provided credential' + e}
            return render(request, 'authentication/login.html', content)


# View to log out members
class LogoutView(FormView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')


class VendorSignUpView(CreateView):
    model = User
    form_class = VendorSignUpForm
    template_name = 'authentication/vendor_signup.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_vendor:
            return redirect(reverse('vendors:vendors-home'))
        content = {'form': VendorSignUpForm}
        return render(request, 'authentication/vendor_signup.html', content)

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'vendor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        vendor = user.vendor
        user.vendor.business_name = form.cleaned_data.get('business_name')
        user.vendor.business_type = form.cleaned_data.get('business_type')
        vendor.business_name = user.vendor.business_name
        vendor.business_type = user.vendor.business_type
        vendor.save()
        login(self.request, user)
        form.send_mail()
        messages.success(self.request,
                         f" Hello {user.vendor.business_name}! Your vendor account with email address {user.email} "
                         f"has been created."
                         )
        return redirect('vendors:vendors-home')


# View for registering customers
class VendeeSignUpView(CreateView):
    model = User
    form_class = VendeeSignUpForm
    template_name = 'authentication/vendee_signup.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_vendee:
            return redirect(reverse('vendee:vendee-home'))
        content = {'form': VendeeSignUpForm}
        return render(request, 'authentication/vendee_signup.html', content)

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'vendee'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        vendee = user.vendee
        vendee.save()
        login(self.request, user)
        form.send_email()
        messages.success(self.request,
                         f" Hello {user.first_name}! Your customer account with email address {user.email} "
                         f"has been created."
                         )
        return redirect('vendee:vendee-home')

    pass


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    form_class = ResetPasswordForm
    template_name = 'authentication/password/password_reset.html'
    email_template_name = 'authentication/password/password_reset_email.html'
    subject_template_name = 'authentication/password/password_reset_subject.txt'
    success_url = reverse_lazy("accounts:password_reset_done")
    pass


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'authentication/password/password_reset_confirm.html'
    success_url = reverse_lazy("accounts:password_reset_complete")

