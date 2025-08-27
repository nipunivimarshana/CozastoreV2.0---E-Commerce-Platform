from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This line correctly points core app for the main page
    path('', include('core.urls')),
]