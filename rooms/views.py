from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView


from .models import Room
from .tables import RoomTable
from .forms import RoomForm
from reservations.models import Reservation


@method_decorator(staff_member_required, name='dispatch')
class RoomListView(ListView):
    template_name = 'generic_templates/list.html'
    model = Room

    def get_queryset(self):
        return self.model.filter_qs(self.request, self.model.objects.all())

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['queryset_table'] = RoomTable(self.object_list)
        context['page_title'] = 'ΔΩΜΑΤΙΑ'
        context['create_url'] = reverse('rooms:create')
        context['search_filter'] = True

        return context


@method_decorator(staff_member_required, name='dispatch')
class RoomCreateView(CreateView):
    template_name = 'generic_templates/form.html'
    form_class = RoomForm
    model = Room
    success_url = reverse_lazy('rooms:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'ΔΗΜΙΟΥΡΓΙΑ ΠΕΛΑΤΗ'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class RoomUpdateView(UpdateView):
    template_name = 'generic_templates/form.html'
    form_class = RoomForm
    model = Room
    success_url = reverse_lazy('rooms:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'ΕΠΕΞΕΡΓΑΣΙΑΣ ΠΕΛΑΤΗ | {self.object}'
        context['back_url'] = self.success_url
        context['delete_url'] = self.object.get_delete_url()

        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class RoomDeleteView(DeleteView):
    success_url = reverse_lazy('rooms:list')
    model = Room
    template_name = 'form_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'ΔΙΑΓΡΑΦΗ ΠΕΛΑΤΗ | {self.object}'
        context['back_url'] = self.success_url
        context['page_title'] = f'ΕΠΑΛΗΘΕΥΣΗ ΔΙΑΓΡΑΦΗΣ | {self.object}'
        context['back_url'] = self.object.get_edit_url()
        return context




@method_decorator(staff_member_required, name='dispatch')
class RoomCardView(DetailView):
    template_name = 'room/room_card.html'
    model = Room

    def get_context_data(self, **kwargs):
        context = super(RoomCardView, self).get_context_data(**kwargs)
        context['page_title'] = f'ΚΑΡΤΕΛΑ {self.object}'
        context['prices'] = self.object.extra_prices.all()
        context['reservations'] = Reservation.filters_data(self.request, self.object.bookings.all())
        active_bookings = self.object.bookings.filter(isDone=False, isCancel=False)
        context['active_reservation'] = active_bookings.last() if active_bookings.exists() else None
        return context
