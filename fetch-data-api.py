"""
Simple API test script to debug authentication
"""
import json
import requests
import hashlib
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastprint_proj.settings')
django.setup()

from products.models import Product, Category, Status

API_URL = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"

def test_api():
    # Step 1: Get server date
    print("Getting server date...")
    response = requests.head(API_URL)
    date_str = response.headers.get('Date')
    cookies = response.cookies

    
    # Parse GMT date and convert to WIB (UTC+7)
    gmt_date = parsedate_to_datetime(date_str)

    wib_tz = timezone(timedelta(hours=7))
    wib_date = gmt_date.astimezone(wib_tz)
    print(f"WIB date: {wib_date.strftime('%d-%m-%Y %H:%M:%S')}")
    
    # Generate credentials
    day = wib_date.day
    month = wib_date.month
    year = str(wib_date.year)[2:]
    
    raw_username = response.headers.get("X-Credentials-Username")
    username = raw_username.split("(")[0].strip()
    password_plain = f"bisacoding-{day:02d}-{month:02d}-{year}"
    password_md5 = hashlib.md5(password_plain.encode()).hexdigest()
    
    print(f"\nCredentials:")
    print(f"Username: {username}")
    print(f"Password plain: {password_plain}")
    print(f"Password MD5: {password_md5}")
    
    # Form data (application/x-www-form-urlencoded)
    print("\nTry 1: Form data")
    payload = {'username': username, 'password': password_md5}
    resp1 = requests.post(API_URL, data=payload, cookies=cookies)
    print(f"Status: {resp1.status_code}")
    print(f"Response: {resp1.text}")
    
    # If successful, save to database
    if resp1.status_code == 200:
        try:
            data = resp1.json()
            if data.get('status') == 'success' or 'data' in data:
                products = data.get('data', [])
                if products:
                    print(f"\n✅ Successfully fetched {len(products)} products!")
                    save_to_database(products)
                else:
                    print("\n⚠️ No products in response")
        except Exception as e:
            print(f"\n❌ Error processing response: {e}")

def save_to_database(products):
    """Delete existing data and insert new data from API"""
    print("\n💾 Saving to database...")
    
    try:
        # Check if there's existing data
        product_count = Product.objects.count()
        category_count = Category.objects.count()
        status_count = Status.objects.count()
        
        print(f"\nExisting data:")
        print(f"  - Products: {product_count}")
        print(f"  - Categories: {category_count}")
        print(f"  - Statuses: {status_count}")
        
        # Delete all existing data
        if product_count > 0 or category_count > 0 or status_count > 0:
            print("\n🗑️ Deleting existing data...")
            Product.objects.all().delete()
            print("  ✓ Deleted all products")
            Category.objects.all().delete()
            print("  ✓ Deleted all categories")
            Status.objects.all().delete()
            print("  ✓ Deleted all statuses")
        
        # Insert new data
        print("\n📥 Inserting new data...")
        
        # Collect unique categories and statuses
        categories = {}
        statuses = {}
        
        for product in products:
            cat_name = product.get('kategori')
            if cat_name and cat_name not in categories:
                categories[cat_name] = None
            
            status_name = product.get('status')
            if status_name and status_name not in statuses:
                statuses[status_name] = None
        
        # Create categories
        for cat_name in categories:
            cat_obj = Category.objects.create(nama_kategori=cat_name)
            categories[cat_name] = cat_obj
            print(f"  ✓ Created category: {cat_name}")
        
        # Create statuses
        for status_name in statuses:
            status_obj = Status.objects.create(nama_status=status_name)
            statuses[status_name] = status_obj
            print(f"  ✓ Created status: {status_name}")
        
        # Create products
        saved_count = 0
        for product in products:
            try:
                Product.objects.create(
                    nama_produk=product.get('nama_produk', ''),
                    harga=float(product.get('harga', 0)),
                    kategori=categories.get(product.get('kategori')),
                    status=statuses.get(product.get('status'))
                )
                saved_count += 1
            except Exception as e:
                print(f"  ⚠️ Error saving product {product.get('nama_produk')}: {e}")
        
        print(f"\n✅ Successfully saved {saved_count} products to database!")
        print(f"\n📊 New database totals:")
        print(f"  - Products: {Product.objects.count()}")
        print(f"  - Categories: {Category.objects.count()}")
        print(f"  - Statuses: {Status.objects.count()}")
        
    except Exception as e:
        print(f"\n❌ Database error: {e}")

if __name__ == '__main__':
    test_api()
