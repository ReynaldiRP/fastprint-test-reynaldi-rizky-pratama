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
    # Only show form (API endpoint handles creation)
    categories = Category.objects.values_list('nama_kategori', flat=True).order_by('nama_kategori')
    
    context = {
        'categories': list(categories),
        'status_choices': ['bisa dijual', 'tidak bisa dijual']
    }
    
    return render(request, 'products/product_form.html', context)

def product_edit(request, product_id):
    """Display form to edit existing product"""
    # Only show form (API endpoint handles update)
    product_obj = get_object_or_404(
        Product.objects.select_related('kategori', 'status'),
        id_produk=product_id
    )
    
    product = {
        'id_produk': product_obj.id_produk,
        'nama_produk': product_obj.nama_produk,
        'harga': float(product_obj.harga),
        'kategori': product_obj.kategori.nama_kategori,
        'status': product_obj.status.nama_status
    }
    
    categories = Category.objects.values_list('nama_kategori', flat=True).order_by('nama_kategori')
    
    context = {
        'product': product,
        'categories': list(categories),
        'status_choices': ['bisa dijual', 'tidak bisa dijual']
    }
    
    return render(request, 'products/product_edit.html', context)

# ============================================
# API ENDPOINTS (Separate from page rendering)
# ============================================

def create_product_api(request):
    """API endpoint to create new product (POST)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body) 
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
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

def update_product_api(request, product_id):
    """API endpoint to update existing product (PUT/PATCH)"""
    if request.method in ['PUT', 'PATCH']:
        try:
            product_obj = get_object_or_404(Product, id_produk=product_id)
            data = json.loads(request.body)
            
            # partial=True for PATCH, False for PUT
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
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

def delete_product_api(request, product_id):
    """API endpoint to delete product (DELETE)"""
    if request.method == 'DELETE':
        try:
            product_obj = get_object_or_404(Product, id_produk=product_id)
            product_obj.delete()
            return JsonResponse({
                'success': True,
                'message': 'Product deleted successfully!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)


