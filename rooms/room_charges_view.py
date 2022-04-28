from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from .models import  RoomCharge, Room
from .tables import RoomChargeTable
from .forms import RoomChargeForm


@method_decorator(staff_member_required, name='dispatch')
class RoomChargeListView(ListView):
    model = RoomCharge
    template_name = 'list_view.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs_table = RoomChargeTable(self.object_list)
        context['create_url'] = reverse('rooms:room_charge_create')
        context['queryset_table'] = qs_table
        context['page_title'] = 'EXTRA'
        return context


@method_decorator(staff_member_required, name='dispatch')
class RoomChargeCreateView(CreateView):
    model = RoomCharge
    form_class = RoomChargeForm
    template_name = 'form_view.html'
    success_url = reverse_lazy('rooms:room_charge_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'ΔΗΜΙΟΥΡΓΙΑ ΝΕΑΣ ΤΙΜΗΣ'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class RoomChargeUpdateView(UpdateView):
    model = RoomCharge
    form_class = RoomChargeForm
    template_name = 'form_view.html'
    success_url = reverse_lazy('rooms:room_charge_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'ΕΠΕΞΕΡΓΑΣΙΑ  ΤΙΜΗΣ {self.object}'
        context['back_url'] = self.success_url
        context['delete_url'] = self.object.get_delete_url()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class RoomChargeDeleteView(DeleteView):
    model = RoomCharge
    form_class = RoomChargeForm
    template_name = 'form_view.html'
    success_url = reverse_lazy('rooms:room_charge_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'ΔΙΑΓΡΑΦΗ  ΤΙΜΗΣ {self.object}'
        context['back_url'] = self.success_url
        return context


@staff_member_required
def room_charge_card_view(request, pk):
    price = get_object_or_404(RoomCharge, id=pk)
    rooms = Room.objects.all()
    back_url = reverse('rooms:room_charge_list')
    return render(request, 'room/room_price_card.html', context=locals())


