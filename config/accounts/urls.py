from django.urls import path

from .views import account_register, account_login, account_logout


urlpatterns = [
    path('register', account_register, name='account_register'),
    path('login', account_login, name='account_login'),
    path('logout', account_logout, name='account_logout'),
]
