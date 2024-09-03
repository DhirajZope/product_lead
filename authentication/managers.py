from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str, **extra_fields):

        if not email:
            raise ValueError("User must have email.")

        if not password:
            raise ValueError("User must have passsword")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError(_("Super user must have is_staff=True"))

        if not extra_fields.get("is_superuser"):
            raise ValueError(_("Super user must have is_superuser=True"))

        if not extra_fields.get("is_active"):
            raise ValueError(_("Super user must have is_active=True"))

        return self.create_user(email, password, **extra_fields)
