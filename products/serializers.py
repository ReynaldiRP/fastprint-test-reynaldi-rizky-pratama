from rest_framework import serializers
from .models import Product, Category, Status


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id_kategori', 'nama_kategori']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id_status', 'nama_status']


class ProductSerializer(serializers.ModelSerializer):
    kategori_nama = serializers.CharField(source='kategori.nama_kategori', read_only=True)
    status_nama = serializers.CharField(source='status.nama_status', read_only=True)
    
    # For create/update, accept category and status as strings
    kategori = serializers.CharField(write_only=True)
    status = serializers.CharField(write_only=True)

    class Meta:
        model = Product
        fields = ['id_produk', 'nama_produk', 'harga', 'kategori', 'status', 'kategori_nama', 'status_nama']
        read_only_fields = ['id_produk']

    def validate_nama_produk(self, value):
        """Validate product name is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Product name cannot be empty")
        return value.strip()

    def validate_harga(self, value):
        """Validate price is positive"""
        if value < 0:
            raise serializers.ValidationError("Price must be a positive number")
        return value

    def create(self, validated_data):
        """Create new product with category and status lookup"""
        kategori_nama = validated_data.pop('kategori')
        status_nama = validated_data.pop('status')
        
        # Get or create category
        kategori, _ = Category.objects.get_or_create(nama_kategori=kategori_nama)
        
        # Get or create status
        status, _ = Status.objects.get_or_create(nama_status=status_nama)
        
        # Create product
        product = Product.objects.create(
            kategori=kategori,
            status=status,
            **validated_data
        )
        
        return product

    def update(self, instance, validated_data):
        """Update existing product"""
        # Handle category update
        if 'kategori' in validated_data:
            kategori_nama = validated_data.pop('kategori')
            kategori, _ = Category.objects.get_or_create(nama_kategori=kategori_nama)
            instance.kategori = kategori
        
        # Handle status update
        if 'status' in validated_data:
            status_nama = validated_data.pop('status')
            status, _ = Status.objects.get_or_create(nama_status=status_nama)
            instance.status = status
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
