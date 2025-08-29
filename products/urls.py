# products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # This will match URLs like /products/classic-white-t-shirt/
    # It captures the slug and passes it to the view.
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]