from django.urls import path

from AdsBoard.views import *

urlpatterns = [
    path('ads/', AdsListView.as_view(), name='ads_list'),
    path('ads/<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('ads/<int:pk>/ad_del_ask/', ad_delete_ask, name='ad_del_ask'),
    path('ads/<int:pk>/ad_del_ask/ad_del_confirm/', ad_delete_confirm, name='ad_del_confirm'),
    path('ads/<int:pk>/repl_del_ask/<int:repl_pk>/', repl_delete_ask, name='repl_del_ask'),
    path('ads/<int:pk>/repl_del_ask/<int:repl_pk>/repl_del_confirm/', repl_delete_confirm, name='repl_del_confirm'),
    path('ads/<int:pk>/repl_apr_and_disapr/<int:repl_pk>/', repl_approve_and_disapprove, name='repl_apr_and_disapr'),
    path('ads/<int:pk>/repl_rej_and_unrej/<int:repl_pk>/', repl_reject_and_unreject, name='repl_rej_and_unrej'),
    path('ads_search/', AdsSearchView.as_view(), name='ads_search'),
    path('ad_create/', AdCreateView.as_view(), name='ad_create'),
    path('ad_update/<int:pk>/', AdUpdateView.as_view(), name='ad_update'),
    path('profile_ads/<int:pk>/', ProfileAdsView.as_view(), name='profile_ads'),
    path('profile_repls/<int:pk>/', ProfileRepliesView.as_view(), name='profile_repls'),
]
