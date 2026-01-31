from datetime import timedelta
import hashlib
from django.shortcuts import render, redirect
import requests
from email.utils import parsedate_to_datetime

# Create your views here.
def product_list(request): 
    products = fetch_api_data()

    context = {
        'products': products,
        'total_count': len(products)
    }

    return render(request, 'products/product_list.html', context)

def product_form(request):
    """Display form to add new product"""
    # Get unique categories from API
    api_data = fetch_api_data_all()
    categories = sorted(set(item['kategori'] for item in api_data if item.get('kategori')))
    
    context = {
        'categories': categories,
        'status_choices': ['bisa dijual', 'tidak bisa dijual']
    }
    
    return render(request, 'products/product_form.html', context)

def fetch_api_data():
    """
    Fetch product data from Fastprint API (only 'bisa dijual' status)
    Returns: list of products or empty list on error
    """
    try:
        session = requests.session()
        resp_get = session.get("https://recruitment.fastprint.co.id/tes/api_tes_programmer")

        server_date = resp_get.headers.get('Date')
        username = resp_get.headers.get('X-Credentials-Username', '').split(' ')[0]

        dt_utc = parsedate_to_datetime(server_date)
        dt_wib = dt_utc + timedelta(hours=7)

        raw_password = f"bisacoding-{dt_wib.day:02d}-{dt_wib.month:02d}-{str(dt_wib.year)[-2:]}"
        md5_password = hashlib.md5(raw_password.encode()).hexdigest()

        response = session.post(
            "https://recruitment.fastprint.co.id/tes/api_tes_programmer",
            data={'username': username, 'password': md5_password}
        )

        if response.status_code == 200:
            data = response.json()
            available_products = [item for item in data.get('data', []) if item.get('status') == 'bisa dijual']

            return available_products  # Return products list
        else:
            print(f"API Error: {response.text}")
            return []
            
    except Exception as e:
        print(f"Error fetching API data: {str(e)}")
        return []

def fetch_api_data_all():
    """
    Fetch ALL product data from Fastprint API (including all statuses)
    Returns: list of all products or empty list on error
    """
    try:
        session = requests.session()
        resp_get = session.get("https://recruitment.fastprint.co.id/tes/api_tes_programmer")

        server_date = resp_get.headers.get('Date')
        username = resp_get.headers.get('X-Credentials-Username', '').split(' ')[0]

        dt_utc = parsedate_to_datetime(server_date)
        dt_wib = dt_utc + timedelta(hours=7)

        raw_password = f"bisacoding-{dt_wib.day:02d}-{dt_wib.month:02d}-{str(dt_wib.year)[-2:]}"
        md5_password = hashlib.md5(raw_password.encode()).hexdigest()

        response = session.post(
            "https://recruitment.fastprint.co.id/tes/api_tes_programmer",
            data={'username': username, 'password': md5_password}
        )

        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        else:
            print(f"API Error: {response.text}")
            return []
            
    except Exception as e:
        print(f"Error fetching API data: {str(e)}")
        return []

