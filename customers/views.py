from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Sum

from .models import Customer, CustomerPayment
from .tables import CustomerTable, PaymentTable
from .forms import CustomerForm, CustomerPaymentForm
from reservations.models import Reservation


@method_decorator(staff_member_required, name='dispatch')
class CostumerListView(ListView):
    template_name = 'generic_templates/list.html'
    model = Customer

    def get_queryset(self):
        return self.model.filter_qs(self.request, self.model.objects.all())

    def get_context_data(self,  **kwargs):
        context = super(CostumerListView, self).get_context_data(**kwargs)
        context['queryset_table'] = CustomerTable(self.object_list)
        context['page_title'] = 'ΠΕΛΑΤΕΣ'
        context['create_url'] = reverse('customers:create')
        context['search_filter'] = True
        return context


@method_decorator(staff_member_required, name='dispatch')
class CustomerCreateView(CreateView):
    template_name = 'generic_templates/form.html'
    form_class = CustomerForm
    model = Customer
    success_url = reverse_lazy('customers:list')

    def get_context_data(self, **kwargs):
        context = super(CustomerCreateView, self).get_context_data(**kwargs)
        context['page_title'] = 'ΔΗΜΙΟΥΡΓΙΑ ΠΕΛΑΤΗ'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        form.save()
        return super(CustomerCreateView, self).form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class CustomerUpdateView(UpdateView):
    template_name = 'generic_templates/form.html'
    form_class = CustomerForm
    model = Customer
    success_url = reverse_lazy('customers:list')

    def get_context_data(self, **kwargs):
        context = super(CustomerUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = f'ΕΠΕΞΕΡΓΑΣΙΑΣ ΠΕΛΑΤΗ | {self.object}'
        context['back_url'] = self.success_url
        context['delete_url'] = self.object.get_delete_url()
        return context

    def form_valid(self, form):
        form.save()
        return super(CustomerUpdateView, self).form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class CustomerDeleteView(DeleteView):
    success_url = reverse_lazy('customers:list')
    model = Customer
    template_name = 'form_view.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = f'ΔΙΑΓΡΑΦΗ ΠΕΛΑΤΗ | {self.object}'
        context['back_url'] = self.success_url
        context['page_title'] = f'ΕΠΑΛΗΘΕΥΣΗ ΔΙΑΓΡΑΦΗΣ | {self.object}'
        context['back_url'] = self.object.get_edit_url()
        return context


@method_decorator(staff_member_required, name='dispatch')
class CustomerCardView(DetailView):
    template_name = 'customers/card.html'
    model = Customer

    def get_context_data(self, **kwargs):
        context = super(CustomerCardView, self).get_context_data(**kwargs)
        context['reservations'] = Reservation.filters_data(self.request, self.object.reservations.all())
        context['payments'] = CustomerPayment.filters_data(self.request, self.object.payments.all())
        return context


@method_decorator(staff_member_required, name='dispatch')
class CustomerPaymentUpdateView(UpdateView):
    model = CustomerPayment
    form_class = CustomerPaymentForm
    template_name = 'form_view.html'

    def get_success_url(self):
        customer = self.object.customer
        return customer.get_card_url()

    def get_context_data(self, **kwargs):
        context = super(CustomerPaymentUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = f'{self.object}'
        context['back_url'] = self.get_success_url()
        context['delete_url'] = self.object.get_delete_url()
        return context


@method_decorator(staff_member_required, name='dispatch')
class CustomerPaymentDeleteView(DeleteView):
    template_name = 'generic_templates/form.html'
    model = CustomerPayment

    def get_success_url(self):
        customer = self.object.customer
        return customer.get_card_url()

    def get_context_data(self, **kwargs):
        context = super(CustomerPaymentDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = f'ΔΙΑΓΡΑΦΗ {self.object}'
        context['back_url'] = self.object.get_edit_url()
        return context


class PaymentListView(ListView):
    template_name = 'generic_templates/list.html'
    model = CustomerPayment
    paginate_by = 50

    def get_queryset(self):
        return self.model.filter_data(self.request, self.model.objects.all())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PaymentListView, self).get_context_data(**kwargs)
        context['page_title'] = 'ΠΛΗΡΩΜΕΣ'
        context['queryset_table'] = PaymentTable(self.object_list)
        context['back_url'] = reverse('homepage')
        qs = self.object_list
        context['total'] = qs.aggregate(Sum('value'))['value__sum'] if qs.exists() else 0
        context['extra_content'], context['search_filter'], context['costumer_filter'], context['date_filter'] = 4*[True]
        return context
