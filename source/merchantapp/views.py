# from conf import tg_bot_token
import datetime

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin

from merchantapp.forms import UserSearchForm, ProgramForm, BranchForm, AddressForm
from merchantapp.models import Program, Branch, Order, UserReward, Merchant


class PermissionAccessMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Merch-man") or \
               self.request.user.groups.filter(name="Stuff")


class CustomerSearchView(PermissionAccessMixin, ListView):
    model = get_user_model()
    template_name = 'index.html'

    def test_func(self):
        return super().test_func() or self.request.user.groups.filter(name="Merch-emp")

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
            queryset = super().get_queryset().filter()
            print('--------------------------------------------------', queryset)
            query = self.get_query()
            queryset = queryset.filter(query)
            return queryset

    def get_query(self):
        query = Q(phone__icontains=self.search_value)
        return query

    def get_search_form(self):
        return UserSearchForm(self.request.GET)

    def get_search_value(self):
        if self.search_form.is_valid():
            return self.search_form.cleaned_data['id']


class CustomerListView(PermissionAccessMixin, ListView):
    model = get_user_model()
    template_name = 'customers/customers_list.html'

    def test_func(self):
        return super().test_func() or self.request.user.groups.filter(name="Merch-emp")

    # def get_queryset(self):
    #     self.queryset = super().get_queryset().filter(
    #                             Order.objects.filter(
    #                             program=Program.objects.filter(
    #                             branch=Branch.objects.filter(
    #                             merchant=Merchant.objects.filter()))))
    #     return self.queryset


class MerchantIndexView(PermissionAccessMixin, TemplateView):
    template_name = 'index.html'

    def test_func(self):
        return super().test_func() or self.request.user.groups.filter(name="Merch-emp")


class ProgramListView(PermissionAccessMixin, ListView):
    model = Program
    template_name = 'program.html'

    def test_func(self):
        return super().test_func() or self.request.user.groups.filter(name="Merch-emp")

    def get_queryset(self):
        return super().get_queryset().filter()


class ProgramCreateView(PermissionAccessMixin, CreateView):
    model = Program
    template_name = 'program_create.html'
    form_class = ProgramForm

    def get_success_url(self):
        return reverse_lazy('merchantapp:programs')


class ProgramUpdateView(PermissionAccessMixin, UpdateView):
    model = Program
    template_name = 'program_update.html'
    form_class = ProgramForm

    def get_success_url(self):
        return reverse_lazy('merchantapp:programs')


class BranchListView(PermissionAccessMixin, ListView):
    model = Branch
    template_name = 'branches/branch_list.html'

    def test_func(self):
        return super().test_func() or self.request.user.groups.filter(name="Merch-emp")

    def get_queryset(self):
        return super().get_queryset().filter()


class BranchCreateView(PermissionAccessMixin, CreateView):
    model = Branch
    template_name = 'branches/branch_create.html'
    form_class = BranchForm

    def get_address_form(self):
        form_kwargs = {}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return AddressForm(**form_kwargs)

    def get_context_data(self, **kwargs):
        if 'address_form' not in kwargs:
            kwargs['address_form'] = self.get_address_form()
        return super().get_context_data(**kwargs)

    def form_valid(self, **kwargs):
        branch = kwargs['form'].save(commit=False)
        address = kwargs['address_form'].save()
        branch.address = address
        branch.save()
        return redirect(self.get_success_url())

    def form_invalid(self, **kwargs):
        context = self.get_context_data(form=kwargs['form'], address_form=kwargs['address_form'])
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = None
        forms = {
            'form': self.get_form(),
            'address_form': self.get_address_form()
        }
        if forms['form'].is_valid() and forms['address_form'].is_valid():
            return self.form_valid(**forms)
        else:
            return self.form_invalid(**forms)

    def get_success_url(self):
        return reverse_lazy('merchantapp:branches')


class BranchUpdateView(PermissionAccessMixin, UpdateView):
    model = Branch
    template_name = 'branches/branch_update.html'
    form_class = BranchForm

    def get_address_form(self):
        form_kwargs = {'instance': self.object.address}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return AddressForm(**form_kwargs)

    def get_context_data(self, **kwargs):
        if 'address_form' not in kwargs:
            kwargs['address_form'] = self.get_address_form()
        return super().get_context_data(**kwargs)

    def form_valid(self, **kwargs):
        branch = kwargs['form'].save(commit=False)
        address = kwargs['address_form'].save()
        branch.address = address
        branch.save()
        return redirect(self.get_success_url())

    def form_invalid(self, **kwargs):
        context = self.get_context_data(form=kwargs['form'], address_form=kwargs['address_form'])
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        forms = {
            'form': self.get_form(),
            'address_form': self.get_address_form()
        }
        if forms['form'].is_valid() and forms['address_form'].is_valid():
            return self.form_valid(**forms)
        else:
            return self.form_invalid(**forms)

    def get_success_url(self):
        return reverse_lazy('merchantapp:branches')


class OrderProcessingView(PermissionAccessMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'

    def test_func(self):
        return super().test_func() or self.request.user.groups.filter(name="Merch-emp")

    def get_queryset(self):
        return super().get_queryset().filter()


class OrderCreateView(PermissionAccessMixin, CreateView):
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
            order.completion_date = timezone.now()
            order.save()
            add_user_reward(customer, order.program)
            send_notification_to_bot(customer, f'Заказ на сумму {order.price * order.amount} тенге выполнен.')
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('merchantapp:merchant_index')


def add_user_reward(customer, program):
    last_obtained_reward = UserReward.objects.filter(user_id=customer).order_by('-time_created').first()
    last_orders_count = Order.objects.filter(user_id=customer,
                                             status='FINISHED',
                                             program=program,
                                             completion_date__gt=last_obtained_reward.time_created
                                             if last_obtained_reward else datetime.datetime(1970, 1, 1)).count()
    if last_orders_count == program.condition.amount:
        UserReward.objects.create(user_id=customer, program=program)
        send_notification_to_bot(customer, 'Получена новая награда!')


def redeem_user_reward(request, **kwargs):
    user = get_user_model().objects.get(pk=kwargs.get('pk'))
    reward = UserReward.objects.filter(user=user, redeemed=False).first()
    if reward:
        reward.redeemed = True
        reward.save()
        send_notification_to_bot(user.id,
                                 'Вы забрали свою награду. Продолжайте выполнять заказы и получайте новые награды!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def access_required(function):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.is_superuser or user.groups.filter('Stuff') or user.groups.filter('Merch-man'):
            return HttpResponseForbidden()
        else:
            return function(request, *args, **kwargs)

    return wrapper


@access_required
def download_customers_file(request, **kwargs):
    file_name = 'customers.csv'
    lines = ['Номер телефона, Всего заказов, Всего наград']
    data = get_user_model().objects.all()
    for d in data:
        lines.append(f'{d.phone}, {d.order_user.count()}, {d.user_reward.count()}')
    response_content = '\n'.join(lines)
    response = HttpResponse(response_content, content_type="text/plain,charset=utf8")
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
    return response


def send_notification_to_bot(user_id, message):
    # user = get_object_or_404(get_user_model(), id=user_id)
    # url = f'https://api.telegram.org/{tg_bot_token}/sendMessage'
    # params = {'chat_id': user.tg_id,
    #           'text': message}
    # r = requests.get(url, params)
    pass
