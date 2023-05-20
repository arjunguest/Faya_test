from django.urls import path
from dashboard import views

urlpatterns = [
    path('register/', views.RegisterApi.as_view(), name='create_customer'),
    path('login/', views.LoginView.as_view(), name='login_customer'),
    path('create_product/', views.ProductCreateView.as_view(), name='Product_list_create'),
    path('product_list/<int:pk>/', views.ProductListUpdateView.as_view(), name='Product_list'),
    path('products/', views.ProductListView.as_view(), name='Products'),
]