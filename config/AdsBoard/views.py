from pprint import pprint

from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView

from .models import *


class AdsListView(ListView):
    model = Adv
    template_name = 'AdsBoard/ads_list.html'
    context_object_name = 'list_of_ads'
    ordering = '-date_of_creation'
    paginate_by = 5
    paginate_orphans = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        pprint(context)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        pprint(queryset)
        return queryset


class AdDetailView(DetailView):
    model = Adv
    template_name = 'AdsBoard/ad_detail.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        pprint(context)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        pprint(queryset)
        return queryset


def ad_delete_ask(request, pk):
    ad = Adv.objects.get(id=pk)
    context = {
        'ad': ad,
        'question': 'Are you sure you want to delete this ad?',
    }
    return render(
        request,
        'AdsBoard/ad_delete.html',
        context=context,
    )


def ad_delete_confirm(request, pk):
    Adv.objects.get(id=pk).delete()
    return redirect(to='ads_list')
