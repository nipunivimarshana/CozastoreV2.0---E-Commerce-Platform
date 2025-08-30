# products/views.py
import json
from django.shortcuts import render
from .models import Product
from django.http import Http404

def product_detail(request, slug):
    # --- DJONGO WORKAROUND to fetch the MAIN product ---
    all_products = Product.objects.all()
    product_list = [p for p in all_products if p.slug == slug and p.is_available]
    if not product_list:
        raise Http404("Product does not exist or is unavailable")
    product = product_list[0]
    # --- END OF WORKAROUND ---

    # --- 1. TEXT-BASED RECOMMENDATIONS (Content Similarity) ---
    try:
        with open('recommendations.json', 'r') as f:
            all_text_recs = json.load(f)
        text_rec_ids = all_text_recs.get(str(product.id), [])
        text_recommended_products = [p for p in all_products if p.id in text_rec_ids]
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback to simple category-based logic
        all_category_products = [p for p in all_products if p.category == product.category and p.is_available and p.id != product.id]
        text_recommended_products = all_category_products[:4]
    
    # --- 2. IMAGE-BASED RECOMMENDATIONS (Visual Similarity) ---
    try:
        with open('visual_recommendations.json', 'r') as f:
            all_visual_recs = json.load(f)
        visual_rec_ids = all_visual_recs.get(str(product.id), [])
        visual_recommended_products = [p for p in all_products if p.id in visual_rec_ids]
    except (FileNotFoundError, json.JSONDecodeError):
        # If visual recommendations don't exist, we can just pass an empty list
        visual_recommended_products = []
    
    # --- 3. PASS EVERYTHING TO THE TEMPLATE ---
    context = {
        'product': product,
        'related_products': text_recommended_products, # The "Related Products" section will use text similarity
        'visual_products': visual_recommended_products, # The new section will use this
    }
    
    return render(request, 'product-detail.html', context)

