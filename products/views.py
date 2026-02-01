from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product, Category
from .serializers import ProductSerializer

# Create your views here.
def product_list(request): 
    """Display list of products with 'bisa dijual' status"""
    products_qs = Product.objects.select_related('kategori', 'status').filter(
        status__nama_status='bisa dijual'
    )
    
    # Convert to dict format for template compatibility
    products = [{
        'id_produk': p.id_produk,
        'nama_produk': p.nama_produk,
        'harga': float(p.harga),
        'kategori': p.kategori.nama_kategori,
        'status': p.status.nama_status
    } for p in products_qs]

    context = {
        'products': products,
        'total_count': len(products)
    }

    return render(request, 'products/product_list.html', context)

def product_form(request):
    """Display form to add new product"""
    if request.method == 'POST':
            try:
                data = json.loads(request.body)
                
                # Validate and create using serializer
                serializer = ProductSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({
                        'success': True,
                        'message': 'Product added successfully!'
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'errors': serializer.errors
                    }, status=400)
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid JSON data'
                }, status=400)
    
    # GET request - show form
    categories = Category.objects.values_list('nama_kategori', flat=True).order_by('nama_kategori')
    
    context = {
        'categories': list(categories),
        'status_choices': ['bisa dijual', 'tidak bisa dijual']
    }
    
    return render(request, 'products/product_form.html', context)

def product_edit(request, product_id):
    """Display form to edit existing product"""
    # Get product from database
    product_obj = get_object_or_404(
        Product.objects.select_related('kategori', 'status'),
        id_produk=product_id
    )
    
    # Handle PUT/PATCH request (RESTful update)
    if request.method in ['PUT', 'PATCH']:
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            
            # Validate and update using serializer
            serializer = ProductSerializer(product_obj, data=data, partial=(request.method == 'PATCH'))
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Product updated successfully!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': serializer.errors
                }, status=400)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            }, status=400)
    
    # GET request - show form with existing data
    product = {
        'id_produk': product_obj.id_produk,
        'nama_produk': product_obj.nama_produk,
        'harga': float(product_obj.harga),
        'kategori': product_obj.kategori.nama_kategori,
        'status': product_obj.status.nama_status
    }
    
    # Get unique categories from database
    categories = Category.objects.values_list('nama_kategori', flat=True).order_by('nama_kategori')
    
    context = {
        'product': product,
        'categories': list(categories),
        'status_choices': ['bisa dijual', 'tidak bisa dijual']
    }
    
    return render(request, 'products/product_edit.html', context)

