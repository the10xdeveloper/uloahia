from django.urls import path

from vendees.views import VendeeHomeView

app_name = 'vendee'

urlpatterns = [

    path('dashboard/', VendeeHomeView.as_view(), name='vendee-home'),

]
