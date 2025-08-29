# users/forms.py

# Import the form we want to use from Django's authentication tools
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # You can add more fields here if you customize your user model later
        # For now, we'll use the default fields that UserCreationForm provides:
        # 1. Username
        # 2. Password
        # 3. Password Confirmation
        
        fields = UserCreationForm.Meta.fields

