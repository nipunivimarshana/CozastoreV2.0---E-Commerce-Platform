from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('blog/', views.blog, name='blog'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.shopping_cart, name='shopping_cart'),
]

# Note: Ensure that 'core' is added to INSTALLED_APPS in settings.py