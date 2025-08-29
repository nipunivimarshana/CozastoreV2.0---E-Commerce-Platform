from django.urls import path
# Import Django's built-in authentication views
from django.contrib.auth import views as auth_views 
# Import our custom register view
from . import views

urlpatterns = [
    # Login Path:
    # We use Django's LoginView and tell it which template to use.
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),

    # Logout Path:
    # Django's LogoutView handles everything for us. It doesn't need a template.
    # After logging out, it will redirect to the LOGOUT_REDIRECT_URL in settings.py (or the homepage by default).
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Registration Path:
    # This path points to the custom 'register' view we created above.
    path('register/', views.register, name='register'),
]