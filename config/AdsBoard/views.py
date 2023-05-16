from pprint import pprint

from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView

from .models import *


class AdsListView(ListView):
    model = Adv
    template_name = 'AdsBoard/ads_list.html'
    context_object_name = 'list_of_ads'
    ordering = '-date_of_creation'
    paginate_by = 2
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
        current_ad = context.get('ad')
        context['replies_to_this_ad'] = current_ad.replies_to_adv.all()
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
    return redirect(
        to='ads_list'
    )


def repl_delete_ask(request, pk, repl_pk):
    ad = Adv.objects.get(id=pk)
    current_repl = ad.replies_to_adv.get(id=repl_pk)
    context = {
        'reply': current_repl,
        'question': 'Are you sure you want to delete this reply?',
    }

    return render(
        request,
        'AdsBoard/reply_delete.html',
        context=context,
    )


def repl_delete_confirm(request, pk, repl_pk):
    ad = Adv.objects.get(id=pk)
    ad.replies_to_adv.get(id=repl_pk).delete()

    return redirect(
        to='ad_detail',
        pk=pk,
    )


def repl_approve_and_disapprove(request, pk, repl_pk):
    ad = Adv.objects.get(id=pk)
    current_repl = ad.replies_to_adv.get(id=repl_pk)

    if not current_repl.is_approved and not current_repl.is_rejected:
        current_repl.approve()
    elif current_repl.is_approved and not current_repl.is_rejected:
        current_repl.disapprove()
    elif not current_repl.is_approved and current_repl.is_rejected:
        current_repl.unreject()
        current_repl.approve()

    return redirect(request.META.get('HTTP_REFERER'))


def repl_reject_and_unreject(request, pk, repl_pk):
    ad = Adv.objects.get(id=pk)
    current_repl = ad.replies_to_adv.get(id=repl_pk)

    if not current_repl.is_rejected and not current_repl.is_approved:
        current_repl.reject()
    elif current_repl.is_rejected and not current_repl.is_approved:
        current_repl.unreject()
    elif not current_repl.is_rejected and current_repl.is_approved:
        current_repl.disapprove()
        current_repl.reject()

    return redirect(request.META.get('HTTP_REFERER'))
