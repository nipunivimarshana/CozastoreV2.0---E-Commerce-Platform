# products/views.py
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.http import Http404 # Import Http404

def product_detail(request, slug):
    # --- DJONGO WORKAROUND ---
    # Step 1: Get ALL products. This is the simplest possible query.
    all_products = Product.objects.all()

    # Step 2: Now, do the filtering in pure Python.
    product_list = [p for p in all_products if p.slug == slug and p.is_available]

    # Step 3: Check if a product was found.
    if not product_list:
        raise Http404("Product does not exist")
    product = product_list[0]
    # --- END OF WORKAROUND ---
    
    # Get related products (other products in the same category)
    related_products = Product.objects.filter(category=product.category, is_available=True).exclude(slug=product.slug)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    
    return render(request, 'product-detail.html', context)
