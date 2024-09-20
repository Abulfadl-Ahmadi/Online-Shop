from .models import User
from django.contrib.auth.backends import ModelBackend


class CustomAuthenticationBackend(ModelBackend):
    """
    Custom authentication backend that distinguishes between incorrect username and incorrect password.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to get the user by username (or email if needed)
            user = User.objects.get(username=username)

            # Check if the password is correct
            if user.check_password(password):
                return user
            else:
                raise ValueError("Incorrect password")
        except User.DoesNotExist:
            raise ValueError("User not found")
