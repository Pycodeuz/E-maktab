from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        # Validate phone number using the specified pattern
        phone_validator = RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits are allowed."
        )
        phone_validator(phone)

        if not password:
            raise ValueError('The Password field must be set')

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        # Create a superuser with additional privileges
        user = self.create_user(phone, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class AdminUser(AbstractBaseUser):
    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits are allowed."
            )
        ]
    )

    full_name = models.CharField(max_length=255)
    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
