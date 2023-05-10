from django.urls import path

from AdsBoard.views import AdsListView


urlpatterns = [
    path('ads/', AdsListView.as_view(), name='ads_list'),
]
