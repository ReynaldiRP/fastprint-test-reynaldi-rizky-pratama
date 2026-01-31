from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.product_form, name='product_add'),
    path('edit/<str:product_id>/', views.product_edit, name='product_edit'),
]