from rest_framework import serializers
from .models import Product
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'], email =  validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

class ProductCreateSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    description = serializers.CharField(style={'base_template': 'textarea.html'})
    is_active = serializers.BooleanField()
    
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    