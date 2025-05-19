from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password = None, **extra_fields):
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(email = email, name = name, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, name, password = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, name, password, **extra_fields)
    
#CustomUser Model
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length = 255, default="Anonymous")
    email = models.EmailField(unique = True)

    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
#EmailOTP Model
class EmailOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    attempts = models.PositiveSmallIntegerField(default=0)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=3)
    
    def has_attempts_left(self):
        return self.attempts < 3

    def __str__(self):
        return f"{self.user.email}"
    
#Blacklist Access Token Model
class BlacklistToken(models.Model):
    jti = models.CharField(max_length = 255, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.jti