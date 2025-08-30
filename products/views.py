# products/views.py
import json
from django.shortcuts import render
from .models import Product
from django.http import Http404

def product_detail(request, slug):
    # --- DJONGO WORKAROUND to fetch the MAIN product ---
    # Step 1: Get ALL products with the simplest possible query.
    all_products = Product.objects.all()

    # Step 2: Filter for the specific product in pure Python.
    product_list = [p for p in all_products if p.slug == slug and p.is_available]

    # Step 3: Check if a product was found, otherwise raise a 404 error.
    if not product_list:
        raise Http404("Product does not exist or is unavailable")
    product = product_list[0]
    # --- END OF WORKAROUND ---

    # --- RECOMMENDATION LOGIC ---
    try:
        with open('recommendations.json', 'r') as f:
            all_recommendations = json.load(f)
        
        recommended_ids = all_recommendations.get(str(product.id), [])
        
        # This part is already using the safe, Python-based filter, which is great.
        recommended_products = [p for p in all_products if p.id in recommended_ids]

    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback logic using a safe Python filter
        all_category_products = [p for p in all_products if p.category == product.category and p.is_available and p.id != product.id]
        recommended_products = all_category_products[:4]
    # --- END OF RECOMMENDATION LOGIC ---
    
    context = {
        'product': product,
        'related_products': recommended_products,
    }
    
    return render(request, 'product-detail.html', context)
