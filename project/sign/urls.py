from allauth.account.views import LogoutView, LoginView
from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from django.urls import path

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='sign/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'),
         name='logout'),
    path('logout/confirmed/', TemplateView.as_view(template_name='sign/logout_confirmed.html'),
         name='logout_confirmed'),
]
