from django.urls import path
from . import views

urlpatterns = [
    # Page rendering endpoints
    path('', views.product_list, name='product_list'),
    path('add/', views.product_form, name='product_add'),
    path('edit/<str:product_id>/', views.product_edit, name='product_edit'),
    
    # API endpoints (RESTful)
    path('api/products/', views.create_product_api, name='api_create_product'),
    path('api/products/<str:product_id>/', views.update_product_api, name='api_update_product'),
    path('api/products/<str:product_id>/delete/', views.delete_product_api, name='api_delete_product'),
]