from django.shortcuts import render
from products.models import Product 


def home(request):
    print("--- HOMEPAGE VIEW: START (ULTRA-SIMPLE METHOD) ---")

    # Step 1: Get ALL products. This is the simplest possible query.
    all_products = Product.objects.all()

    # Step 2: Now, do the filtering and sorting in pure Python.
    # This happens in memory, not in the database query.
    available_products = [p for p in all_products if p.is_available]
    
    # The 'key' tells Python to sort based on the 'created_at' attribute.
    # 'reverse=True' makes it descending (newest first).
    sorted_products = sorted(available_products, key=lambda p: p.created_at, reverse=True)

    # Step 3: Finally, slice the Python list.
    products = sorted_products[:8]
    
    print(f"--- PRODUCTS FOUND: {len(products)} ---")
    
    # This dictionary will pass the data to the template.
    context = {
        'products': products
    }

    return render(request, "index.html")

def shop(request):
    return render(request, "product.html")

def blog(request):
    return render(request, "blog.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def shopping_cart(request):
    return render(request, "shoping-cart.html")
