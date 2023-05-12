from django.urls import path

from AdsBoard.views import AdsListView, AdDetailView, adv_delete

urlpatterns = [
    path('ads/', AdsListView.as_view(), name='ads_list'),
    path('ads/<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('ads/<int:pk>/ad_del/', adv_delete, name='ad_del'),
    # path('ads/<int:pk>/repl_del', repl_delete, name='repl_del'),
]
