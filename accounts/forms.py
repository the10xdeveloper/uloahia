from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, \
    AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.template import loader
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.models import Vendor, Vendee, Address
from ahia.settings import DEFAULT_FROM_EMAIL, SUPPORT_FROM_EMAIL
from malls import MallTypeKind

User = get_user_model()


# Account authentication forms

# Form for loging in users

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


class VendorSignUpForm(UserCreationForm):
    business_name = forms.CharField(widget=forms.TextInput(attrs=({'class': 'form-control'})))
    business_type = forms.ChoiceField(choices=MallTypeKind.CHOICES)

    # slug = forms.SlugField(widget=forms.HiddenInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(VendorSignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['business_type'].widget.attrs.update({'class': 'form-control'})

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_vendor = True
        user.save()
        vendor = Vendor.objects.create(user=user)
        return user

    def send_mail(self):
        subject = render_to_string("emails/vendor/vendor_welcome_subject.txt").strip()
        text_body = render_to_string("emails/vendor/vendor_welcome_email.txt")
        html_body = render_to_string("emails/vendor/vendor_welcome_email.html")
        from_email = DEFAULT_FROM_EMAIL
        to_email = self.cleaned_data['email']
        email_message = EmailMultiAlternatives(subject=subject, body=html_body,
                                               from_email=from_email, to=[to_email])
        email_message.attach_alternative(html_body, "text/html")
        email_message.send()


class VendeeSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(VendeeSignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_vendee = True
        user.save()
        vendee = Vendee.objects.create(user=user)
        return user

    def send_email(self):
        email_subject = render_to_string("emails/vendee/vendee_welcome_subject.txt").strip()
        text_body = render_to_string("emails/vendee/vendee_welcome_email.txt")
        html_body = render_to_string("emails/vendee/vendee_welcome_email.html")
        sender_email = DEFAULT_FROM_EMAIL
        recipients_email = self.cleaned_data['email']
        email_message = EmailMultiAlternatives(subject=email_subject, body=html_body,
                                               from_email=sender_email, to=[recipients_email])
        email_message.attach_alternative(html_body, "text/html")
        email_message.send()


class ResetPasswordForm(PasswordResetForm):

    def send_mail(
            self,
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = render_to_string(email_template_name, context)
        from_email = SUPPORT_FROM_EMAIL

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        email_message.attach_alternative(body, "text/html")

        email_message.send()


class CreateAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
