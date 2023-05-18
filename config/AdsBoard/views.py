from pprint import pprint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import AdvForm, ReplyForm
from .models import *
from .filters import AdvFilter


class AdsListView(ListView):
    # model = Adv
    template_name = 'AdsBoard/ads_list.html'
    context_object_name = 'list_of_ads'
    paginate_by = 1
    paginate_orphans = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        pprint(context)
        return context

    def get_queryset(self):
        # здесь мы уменьшаем количество запросов в БД через select_related для оптимизации нагрузки на СУБД
        queryset = Adv.objects.all().order_by('-date_of_creation').select_related('author')
        pprint(queryset)
        return queryset


class AdsSearchView(ListView):
    model = Adv
    template_name = 'AdsBoard/ads_search.html'
    ordering = '-date_of_creation'
    context_object_name = 'search_ads'
    paginate_by = 1
    paginate_orphans = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['querydict'] = self.request.GET.dict()
        pprint(context)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdvFilter(self.request.GET, queryset)
        pprint(self.filterset)
        return self.filterset.qs


class AdDetailView(DetailView, CreateView):
    model = Adv
    template_name = 'AdsBoard/ad_detail.html'
    context_object_name = 'ad'
    form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        current_ad = context.get('ad')
        context['replies_to_this_ad'] = current_ad.replies_to_adv.all()
        context['current_user_left_reply'] =\
            context['replies_to_this_ad'].filter(author=self.request.user).exists()
        pprint(context)
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('ad_detail', kwargs={'pk': f'{self.object.adv.pk}'})

    def form_valid(self, form, **kwargs):
        repl = form.save(commit=False)
        repl.author = self.request.user
        repl.adv = Adv.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)


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


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Adv
    form_class = AdvForm
    template_name = 'AdsBoard/ad_create_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        pprint(context)
        return context

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ad_detail', kwargs={'pk': self.object.pk})


class AdUpdateView(UpdateView):
    model = Adv
    form_class = AdvForm
    template_name = 'AdsBoard/ad_create_edit.html'

    def get_success_url(self):
        return reverse('ad_detail', kwargs={'pk': self.object.pk})
