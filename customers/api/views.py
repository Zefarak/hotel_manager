from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import  SearchFilter, OrderingFilter
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from ..models import Customer, CustomerPayment
from .serializers import CustomerDetailSerializer, CustomerListSerializer, CostumerPaymentSerializer


@api_view(['GET', ])
def customers_homepage_view(request, format=None):
    return Response({
        'list': reverse('api_customers:list', request=request, format=format),
        'payments': reverse('api_customers:payment_list', request=request, format=format),
        
    })


class CustomerListCreateApiView(ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['repeater', ]
    search_fields = ['title', 'phone', 'email']
    ordering_filters = ['title', 'balance']
    

class CustomerDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerDetailSerializer
    permission_classes = [IsAuthenticated, ]


class PaymentCreateListApiView(ListCreateAPIView):
    queryset = CustomerPayment.objects.all()
    serializer_class = CostumerPaymentSerializer