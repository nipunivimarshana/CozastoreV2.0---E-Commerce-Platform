from django.shortcuts import render
from products.models import Product # This import is correct and necessary

# --- CORRECTED home VIEW ---
def home(request):
    # This is the "ultra-simple" method that is confirmed to work with Djongo
    all_products = Product.objects.all()
    available_products = [p for p in all_products if p.is_available]
    sorted_products = sorted(available_products, key=lambda p: p.created_at, reverse=True)
    products = sorted_products[:8]
    
    context = {
        'products': products
    }
    return render(request, "index.html", context)


# --- CORRECTED shop VIEW ---
def shop(request):
    # We will use the same ultra-simple method here to avoid Djongo bugs
    all_products = Product.objects.all()
    products = [p for p in all_products if p.is_available]
    
    context = {
        'products': products
    }
    return render(request, "product.html", context)


# --- The rest of your views are for static pages and are correct ---
def blog(request):
    return render(request, "blog.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def shopping_cart(request):
    return render(request, "cart/detail.html")