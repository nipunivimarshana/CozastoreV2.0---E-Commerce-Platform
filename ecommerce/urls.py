from django.contrib import admin
from django.urls import path, include

# These two imports are required for serving user-uploaded media files
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Path for the Django admin site
    path('admin/', admin.site.urls),

    # This will handle URLs like /accounts/login/, /accounts/signup/
    # It must appear only ONCE.
    path('accounts/', include('users.urls', namespace='users')),

    # This will handle the URL for the product detail page (e.g., /products/classic-white-t-shirt/)
    path('products/', include('products.urls', namespace='products')),

    # This must come LAST. It handles the homepage (''), /shop/, /about/, etc.
    path('', include('core.urls')),
]

# This line is CRITICAL for making your product images appear during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)