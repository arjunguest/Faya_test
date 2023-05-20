from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from django.utils import timezone

from dashboard.models import Product
from django.contrib.auth.models import User

from dashboard.serializers import ProductCreateSerializer,RegisterSerializer,LoginSerializer,ProductListSerializer


class RegisterApi(APIView):
    api_view = ['POST']
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(username = serializer.data['username'])
                token_obj, create = Token.objects.get_or_create(user=user)
                return Response({'payload':serializer.data,'token':token_obj.key, 'message':"User registered successfully"}, status = status.HTTP_200_OK)
            else:
                return Response({'status':403, 'errors': serializer.errors,'message':"Error registering user"})
        except Exception as e:
            print("Error--------:",str(e))
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)
        
        
class LoginView(APIView):
    api_view = ['POST']
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'payload':serializer.data,'token':token.key, 'message':"Login successfully"}, status = status.HTTP_200_OK)
                else:
                    return Response({'message': 'Invalid credentials.'}, status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': ' Please fill vaild data'}, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Error--------:",str(e))
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

class ProductCreateView(APIView):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductCreateSerializer
    
    def post(self, request):
        try:
            user = request.user.id
            customer = User.objects.filter(id=user).last()
            serializer = ProductCreateSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                product= Product.objects.create(
                    product_name = serializer.validated_data['product_name'],
                    description = serializer.validated_data['description'],
                    is_active = serializer.validated_data['is_active'],
                    created_at = timezone.now(),
                    customer = customer
                    )
                product.save()
                return Response({'payload':serializer.data,'message':" Product added successfully"}, status = status.HTTP_200_OK)
            else:
                return Response({'message': ' Please fill vaild data'}, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Error--------:",str(e))
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

class ProductListUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    lookup_field = 'pk'

    def perform_update(self, serializer):
        product = self.get_object()
        if (timezone.localtime(timezone.now()) - product.created_at).days > 60:
            serializer.save(is_active=False)
            return Response("Product disabled")
        else:
            serializer.save()
            return Response("Product can only be disabled if registered before 2 months.")
            
class ProductListView(APIView):
    api_view = ['GET']
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    serializer_class = ProductListSerializer
    
    def get(self, request):
        try:
            data = Product.objects.all()
            if data :
                serializer = ProductListSerializer(data,many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error':'No data found'},status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Error--------:",str(e))
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)