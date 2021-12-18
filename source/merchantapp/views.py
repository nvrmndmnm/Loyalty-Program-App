from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, TemplateView, CreateView
from merchantapp.forms import UserSearchForm
from merchantapp.models import Program, Branch, Order, UserReward


class CustomerSearchView(ListView):
    model = get_user_model()
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        self.search_form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_form'] = self.search_form
        if self.search_value:
            context['query'] = urlencode({'id': self.search_value})
        return context

    def get_queryset(self):
        if self.search_value:
            queryset = super().get_queryset()
            query = self.get_query()
            queryset = queryset.filter(query)
            return queryset

    def get_query(self):
        query = Q(username__icontains=self.search_value)
        return query

    def get_search_form(self):
        return UserSearchForm(self.request.GET)

    def get_search_value(self):
        if self.search_form.is_valid():
            return self.search_form.cleaned_data['id']


class MerchantIndexView(TemplateView):
    template_name = 'index.html'


class ProgramListView(ListView):
    model = Program
    template_name = 'program.html'


class ProgramCreateView(CreateView):
    model = Program
    template_name = 'program_create.html'
    fields = ['title', 'condition', 'reward']


class BranchListView(ListView):
    model = Branch
    template_name = 'branches/branch_list.html'


class BranchCreateView(CreateView):
    model = Branch
    template_name = 'branches/branch_create.html'
    fields = ['name', 'address']


class OrderProcessingView(ListView):
    model = Order
    template_name = 'orders/order_list.html'


class OrderCreateView(CreateView):
    model = Order
    template_name = 'orders/order_create.html'
    fields = ['price', 'amount', 'program']
    success_url = ''

    def form_valid(self, form):
        order = form.save(commit=False)
        customer = self.request.GET.get('customer', '')
        if customer:
            order.user_id = customer
            order.status = 'FINISHED'
            order.completion_date = datetime.now()
            order.save()
        else:
            self.form_invalid(form)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('merchantapp:merchant_index')


def redeem_user_reward(request, **kwargs):
    user = get_user_model().objects.get(pk=kwargs.get('pk'))
    reward = UserReward.objects.filter(user=user, redeemed=False).first()
    if reward:
        reward.redeemed = True
        reward.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
