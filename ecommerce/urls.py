from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # This line correctly points core app for the main page
    path('', include('core.urls')),
    # This will create URLs like /accounts/login/, /accounts/register/, etc.
     path('accounts/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# --------------------------------------------------