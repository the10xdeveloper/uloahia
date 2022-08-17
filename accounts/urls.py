from django.urls import path

from accounts.views import LoginView, LogoutView, VendeeSignUpView, VendorSignUpView, ResetPasswordView, \
    ResetPasswordConfirmView
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [

    path('login/', LoginView.as_view(), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),

    # path('password_reset/',
    #      auth_views.PasswordResetView.as_view(template_name='authentication/password/password_reset.html'),
    #      name='password_reset_done'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='authentication/password/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password/password_reset_complete'
                                                                    '.html'),
         name='password_reset_complete'),

    path('vendor/signup/', VendorSignUpView.as_view(), name='vendor_signup'),

    path('vendee/signup/', VendeeSignUpView.as_view(), name='vendee_signup'),

]

# accounts / login / [name = 'login']
# accounts / logout / [name = 'logout']
# accounts / password_change / [name = 'password_change']
# accounts / password_change / done / [name = 'password_change_done']
# accounts / password_reset / [name = 'password_reset']
# accounts / password_reset / done / [name = 'password_reset_done']
# accounts / reset / < uidb64 > / < token > / [name = 'password_reset_confirm']
# accounts / reset / done / [name = 'password_reset_complete']
