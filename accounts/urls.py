from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^register$', views.RegistrationView.as_view(), name='registration'),
    url(r'^$', views.LoginView.as_view(), name='login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^account$', views.AccountView.as_view(), name='account'),
    url(r'^account/update-profile$', views.UpdateAccountView.as_view(), name='update_account'),
    url(r'^account/update-password$', views.UpdatePasswordView.as_view(), name='update_password'),
    url(r'^account/payroll$', views.PayrollView.as_view(), name='payroll'),
    url(r'^account/payroll/add', views.AddPayrollView.as_view(), name='add-payroll')
]