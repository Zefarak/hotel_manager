from rest_framework import serializers

from ..models import Customer, CustomerPayment


class CustomerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'title', 'phone', 'email', 'balance']


class CustomerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'



class CostumerPaymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomerPayment
        fields = '__all__'