# products/views.py
from django.shortcuts import render, get_object_or_404
from .models import Product, Category # Import your models

def product_detail(request, slug):
    # Fetch the specific product from the database using the slug from the URL.
    # It will only find products that are marked as available.
    # If no product is found, it will automatically raise a 404 Page Not Found error.
    product = get_object_or_404(Product, slug=slug, is_available=True)
    
     # Get related products from the same category.
    # Exclude the current product from the list.
    # Limit the results to the first 4 products.
    related_products = Product.objects.filter(category=product.category, is_available=True).exclude(slug=product.slug)[:4]
    # --------------------
    
    # This dictionary passes the found product object to the template.
    context = {
        'product': product,
        'related_products': related_products
    }
    
    return render(request, 'product-detail.html', context)