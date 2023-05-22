from django.urls import path

from .views import account_register, account_login, account_logout, account_confirm


urlpatterns = [
    path('register/', account_register, name='account_register'),
    path('confirm/', account_confirm, name='account_confirm'),
    path('login/', account_login, name='account_login'),
    path('logout/', account_logout, name='account_logout'),
]
