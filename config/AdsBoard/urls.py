from django.urls import path

from AdsBoard.views import AdsListView, AdDetailView

urlpatterns = [
    path('ads/', AdsListView.as_view(), name='ads_list'),
    path('ads/<int:pk>', AdDetailView.as_view(), name='ad_detail'),
]
