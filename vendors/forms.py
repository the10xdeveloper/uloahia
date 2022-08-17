import datetime

from django import forms
from django.contrib.auth import get_user_model

from accounts.models import Vendor, Address

User = get_user_model()


class WebUserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'birth_date', 'gender',)

    def __init__(self, *args, **kwargs):
        super(WebUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['avatar'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['birth_date'].widget.attrs.update({'class': 'form-control vDateField datepicker-input'})


class VendorUpdateForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ('business_name', 'business_type',)

    def __init__(self, *args, **kwargs):
        super(VendorUpdateForm, self).__init__(*args, **kwargs)
        self.fields['business_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['business_type'].widget.attrs.update({'class': 'form-control'})

