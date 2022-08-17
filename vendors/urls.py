from django.urls import path

from vendors.views import VendorsHomeView, VendorUpdateView, VendorDetailView, VendorCatalogHomeView

app_name = 'vendors'
urlpatterns = [

    path('dashboard/', VendorsHomeView.as_view(), name='vendors-home'),

    path('catalog/', VendorCatalogHomeView.as_view(), name='vendors-catalog'),

    path('<int:pk>/<uuid>/update/', VendorUpdateView.as_view(), name='vendors-update'),

    path('detail/', VendorDetailView.as_view(), name='vendors-detail')

]
