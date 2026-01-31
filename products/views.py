from datetime import datetime, timedelta
import hashlib
from django.shortcuts import render
import requests
from email.utils import parsedate_to_datetime

# Create your views here.
def product_list(request): 
    products = fetch_api_data()

    context = {
        'products': products[:5],
        'total_count': len(products)
    }

    return render(request, 'products/product_list.html', context)

def fetch_api_data():
    """
    Fetch product data from Fastprint API
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

        print(f"API Response Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])  # Return products list
        else:
            print(f"API Error: {response.text}")
            return []
            
    except Exception as e:
        print(f"Error fetching API data: {str(e)}")
        return []

