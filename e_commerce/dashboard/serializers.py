from rest_framework import serializers
from .models import Product,Customer
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        customer = Customer(**validated_data)
        customer.set_password(password)
        customer.save()
        return customer

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

class ProductCreateSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    description = serializers.CharField(style={'base_template': 'textarea.html'})
    is_active = serializers.BooleanField()
    
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    