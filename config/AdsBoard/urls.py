from django.urls import path

from AdsBoard.views import (
    AdsListView, AdDetailView,
    ad_delete_ask, ad_delete_confirm,
)

urlpatterns = [
    path('ads/', AdsListView.as_view(), name='ads_list'),
    path('ads/<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('ads/<int:pk>/ad_del_ask/', ad_delete_ask, name='ad_del_ask'),
    path('ads/<int:pk>/ad_del_ask/ad_del_confirm', ad_delete_confirm, name='ad_del_confirm'),
]
