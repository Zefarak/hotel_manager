from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from .models import RoomPrice, Room
from .tables import RoomPriceTable
from .forms import RoomPriceForm_


@method_decorator(staff_member_required, name='dispatch')
class RoomPriceListView(ListView):
    model = RoomPrice
    template_name = 'list_view.html'
    paginate_by = 30

    def get_context_data(self,  **kwargs):
        context = super(RoomPriceListView, self).get_context_data(**kwargs)
        qs_table = RoomPriceTable(self.object_list)
        context['create_url'] = reverse('rooms:room_price_create')
        context['queryset_table'] = qs_table
        context['page_title'] = 'ΤΙΜΕΣ ΔΩΜΑΤΙΩΝ'
        return context


@method_decorator(staff_member_required, name='dispatch')
class RoomPriceCreateView(CreateView):
    model = RoomPrice
    form_class = RoomPriceForm_
    template_name = 'form_view.html'
    success_url = reverse_lazy('rooms:room_price_list')
    
    def get_context_data(self, **kwargs):
        context = super(RoomPriceCreateView, self).get_context_data(**kwargs)
        context['page_title'] = 'ΔΗΜΙΟΥΡΓΙΑ ΝΕΑΣ ΤΙΜΗΣ'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        form.save()
        return super(RoomPriceCreateView, self).form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class RoomPriceUpdateView(UpdateView):
    model = RoomPrice
    form_class = RoomPriceForm_
    template_name = 'form_view.html'
    success_url = reverse_lazy('rooms:room_price_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'ΕΠΕΞΕΡΓΑΣΙΑ  ΤΙΜΗΣ {self.object}'
        context['back_url'] = self.success_url
        context['delete_url'] = self.object.get__delete_url()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class RoomPriceDeleteView(DeleteView):
    model = RoomPrice
    form_class = RoomPriceForm_
    template_name = 'form_view.html'
    success_url = reverse_lazy('rooms:room_price_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'ΔΙΑΓΡΑΦΗ  ΤΙΜΗΣ {self.object}'
        context['back_url'] = self.success_url
        return context


@staff_member_required
def room_price_card_view(request, pk):
    price = get_object_or_404(RoomPrice, id=pk)
    rooms = Room.objects.all()
    back_url = reverse('rooms:room_price_list')
    return render(request, 'room/room_price_card.html', context=locals())


