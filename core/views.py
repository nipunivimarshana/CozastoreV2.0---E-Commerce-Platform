from django.shortcuts import render

def home(request):
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
