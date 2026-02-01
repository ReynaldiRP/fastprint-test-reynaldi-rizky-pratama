# Fastprint Test Project - Reynaldi Rizky Pratama

A Django-based web application for managing products with full CRUD operations, built with Django REST Framework and PostgreSQL.

## 📋 Requirements Met

This project fulfills all requirements for the Junior Programmer Test:
- ✅ Fetch data from API
- ✅ Create database tables (Product, Category, Status)
- ✅ Save API data to database
- ✅ Display products with "bisa dijual" status
- ✅ CRUD features (Create, Read, Update, Delete)
- ✅ Form validation (name required, price must be number)
- ✅ Delete confirmation alert
- ✅ Django framework with Serializers
- ✅ PostgreSQL database

## 🚀 Technology Stack

- **Backend:** Django 5.2.10
- **API:** Django REST Framework 3.16.1
- **Database:** PostgreSQL 16
- **Frontend:** HTML, Tailwind CSS (CDN), Vanilla JavaScript
- **Python:** 3.10.6

## 📦 Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/ReynaldiRP/fastprint-test-reynaldi-rizky-pratama.git
cd test-fastprint
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install django==5.2.10
pip install djangorestframework==3.16.1
pip install psycopg2-binary
```

## 🗄️ Database Setup

### 1. Create PostgreSQL Database
```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE "test-fastprint";

# Exit PostgreSQL
\q
```

### 2. Configure Database Connection
Update `fastprint_proj/settings.py` if needed (default settings):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test-fastprint',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Populate Database from API

**Option A: Run Python Script**
```bash
python testing-api.py
```
This will fetch data from the API and display it. Then execute the generated SQL inserts.

**Option B: Use SQL Script**
```bash
psql -U postgres -d test-fastprint -f insert_data.sql
```

### 5. Verify Data
```bash
python manage.py shell
```
```python
from products.models import Product, Category, Status
print(f"Products: {Product.objects.count()}")
print(f"Categories: {Category.objects.count()}")
print(f"Statuses: {Status.objects.count()}")
```

## ▶️ Running the Application

### 1. Start PostgreSQL Service
```bash
# Windows
net start postgresql-x64-16

# Linux
sudo systemctl start postgresql
```

### 2. Start Django Development Server
```bash
python manage.py runserver
```

### 3. Access Application
Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

## 🎯 Feature Walkthrough

### 1. **Product List Page** (`/`)
- Displays all products with status "bisa dijual"
- Shows product name, price, category, and status
- Grid layout (3 columns on desktop, responsive)
- Formatted price with thousand separator (Rp 25,000)

**Actions:**
- **Add Product**: Click "Add Product" button in top-right
- **Edit Product**: Click "Edit" button on any product card
- **Delete Product**: Click "Delete" button (shows confirmation alert)

### 2. **Add Product** (`/add/`)
- Form with 4 fields:
  - Product Name (text, required)
  - Price (number, required, positive values only)
  - Category (dropdown, populated from database)
  - Status (dropdown: "bisa dijual" or "tidak bisa dijual")

**Validation:**
- Client-side: JavaScript checks before submission
- Server-side: Django serializer validates data
- Shows error messages for invalid input

**How it works:**
1. Fill in all fields
2. Click "Add Product"
3. JavaScript sends POST request to `/api/products/`
4. On success: Shows alert and redirects to product list
5. On error: Shows validation errors

### 3. **Edit Product** (`/edit/<id>/`)
- Pre-filled form with existing product data
- Same validation as Add form
- Uses RESTful PUT method

**How it works:**
1. Modify any field
2. Click "Update Product"
3. JavaScript sends PUT request to `/api/products/<id>/`
4. On success: Shows alert and redirects to product list
5. On error: Shows validation errors

### 4. **Delete Product**
- Available from product list page
- Shows confirmation dialog: "Are you sure you want to delete [Product Name]?"
- Cannot be undone

**How it works:**
1. Click "Delete" button on product card
2. Confirmation dialog appears
3. If confirmed: JavaScript sends DELETE request to `/api/products/<id>/delete/`
4. On success: Reloads page to show updated list

## 🔌 API Endpoints

### Base URL: `http://127.0.0.1:8000`

### Product Endpoints

#### 1. Create Product
```http
POST /api/products/
Content-Type: application/json
X-CSRFToken: <csrf-token>

{
  "nama_produk": "Product Name",
  "harga": 25000,
  "kategori": "Category Name",
  "status": "bisa dijual"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Product added successfully!"
}
```

**Response (Error):**
```json
{
  "success": false,
  "errors": {
    "nama_produk": ["Nama produk tidak boleh kosong"],
    "harga": ["Harga tidak boleh negatif"]
  }
}
```

#### 2. Update Product (Full Update)
```http
PUT /api/products/<id>/
Content-Type: application/json
X-CSRFToken: <csrf-token>

{
  "nama_produk": "Updated Name",
  "harga": 30000,
  "kategori": "New Category",
  "status": "tidak bisa dijual"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Product updated successfully!"
}
```

#### 3. Update Product (Partial Update)
```http
PATCH /api/products/<id>/
Content-Type: application/json
X-CSRFToken: <csrf-token>

{
  "harga": 35000
}
```

#### 4. Delete Product
```http
DELETE /api/products/<id>/delete/
X-CSRFToken: <csrf-token>
```

**Response:**
```json
{
  "success": true,
  "message": "Product deleted successfully!"
}
```

### Page Endpoints (HTML)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Product list page |
| GET | `/add/` | Add product form |
| GET | `/edit/<id>/` | Edit product form |
| GET | `/admin/` | Django admin panel |

## 🧪 Testing the API

### Using curl

**Create Product:**
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "nama_produk": "Test Product",
    "harga": 15000,
    "kategori": "Electronics",
    "status": "bisa dijual"
  }'
```

**Update Product:**
```bash
curl -X PUT http://127.0.0.1:8000/api/products/P001/ \
  -H "Content-Type: application/json" \
  -d '{
    "nama_produk": "Updated Product",
    "harga": 20000,
    "kategori": "Electronics",
    "status": "bisa dijual"
  }'
```

**Delete Product:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/products/P001/delete/
```

## 📁 Project Structure

```
test-fastprint/
├── fastprint_proj/          # Django project settings
│   ├── settings.py          # Database, installed apps
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py
├── products/                # Main application
│   ├── models.py            # Database models (Product, Category, Status)
│   ├── serializers.py       # DRF serializers with validation
│   ├── views.py             # Views and API endpoints
│   ├── urls.py              # App URL patterns
│   ├── admin.py             # Django admin configuration
│   └── templates/
│       └── products/
│           ├── base.html           # Base template
│           ├── product_list.html   # Product list page
│           ├── product_form.html   # Add product form
│           └── product_edit.html   # Edit product form
├── testing-api.py           # Script to fetch API data
├── insert_data.sql          # SQL script to populate database
├── manage.py                # Django management script
└── README.md                # This file
```

## 🔐 External API Details

**API URL:** `https://recruitment.fastprint.co.id/tes/api_tes_programmer`

**Authentication:**
- Username: `tesprogrammer010226C08` (changes with server time)
- Password: MD5 hash of `bisacoding-DD-MM-YY` format
  - Example for 01 Feb 2026: `bisacoding-01-02-26`
  - Script automatically generates correct password based on server date

**How to Test API:**
```bash
python testing-api.py
```

## 🛠️ Database Schema

### Product Table
```sql
Column       | Type          | Constraints
-------------|---------------|-------------
id_produk    | VARCHAR(50)   | PRIMARY KEY
nama_produk  | VARCHAR(255)  | NOT NULL
harga        | DECIMAL(10,2) | NOT NULL
kategori_id  | INT           | FOREIGN KEY -> Category
status_id    | INT           | FOREIGN KEY -> Status
```

### Category Table
```sql
Column         | Type         | Constraints
---------------|--------------|-------------
id_kategori    | SERIAL       | PRIMARY KEY
nama_kategori  | VARCHAR(100) | NOT NULL
```

### Status Table
```sql
Column       | Type         | Constraints
-------------|--------------|-------------
id_status    | SERIAL       | PRIMARY KEY
nama_status  | VARCHAR(50)  | NOT NULL
```
---

**Created by:** Reynaldi Rizky Pratama  
**Date:** February 2026  
**Test:** Junior Programmer - Fastprint
