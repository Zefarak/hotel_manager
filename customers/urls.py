from django.urls import path

from .views import (CostumerListView, CustomerCreateView,
                    CustomerUpdateView, CustomerDeleteView, CustomerCardView,
                    CustomerPaymentUpdateView, CustomerPaymentDeleteView,
                    PaymentListView
                    )


app_name = 'customers'

urlpatterns = [
    path('list/', CostumerListView.as_view(), name='list'),
    path('create/', CustomerCreateView.as_view(), name='create'),
    path('update/<int:pk>/', CustomerUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', CustomerDeleteView.as_view(), name='delete'),
    path('card/<int:pk>/', CustomerCardView.as_view(), name='card'),

    path('payment/update/<int:pk>/', CustomerPaymentUpdateView.as_view(), name='payment_update'),
    path('payment/delete/<int:pk>/', CustomerPaymentDeleteView.as_view(), name='payment_delete'),
    path('payment-list/', PaymentListView.as_view(), name='payment_list')
]