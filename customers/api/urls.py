from django.urls import path

from .views import (
    CustomerListCreateApiView, CustomerDetailApiView, PaymentCreateListApiView,
    customers_homepage_view
    )

app_name = 'api_customers'

urlpatterns = [
    path('', customers_homepage_view, name='home'),
    path('list/', CustomerListCreateApiView.as_view(), name='list'),
    path('detail/<int:pk>/', CustomerDetailApiView.as_view, name='detail'),
    path('payment/list/', PaymentCreateListApiView.as_view(), name='payment_list')

]