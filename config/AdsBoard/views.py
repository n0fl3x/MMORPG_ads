from django.views.generic import ListView

from .models import *


class AdsListView(ListView):
    model = Adv
    template_name = 'AdsBoard/ads_list.html'
    context_object_name = 'list_of_ads'
    ordering = '-date_of_creation'
    paginate_by = 5
    paginate_orphans = 1
