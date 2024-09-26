from rest_framework import serializers
from .models import Customers

class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        # fields = ['id', 'name', 'price', 'quantity', 'description']
        fields = '__all__'  # Include all fields by default
