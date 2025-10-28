from django.db import models
from django.utils import timezone
from auditlog.registry import auditlog
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, name, password, **extra_fields)


# CustomUser Model
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, default="Anonymous")
    # username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Login failed attempts
    failed_login_attempts = models.IntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name if self.name else self.email


# Register User model for audit logging
auditlog.register(User)


# User Device Model
class UserDevice(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='devices')
    device_info = models.TextField()
    ip_address = models.GenericIPAddressField()
    last_used = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('user', 'device_info', 'ip_address')  # Avoid duplicates

    def __str__(self):
        return f"{self.user.email} - {self.device_info} - {self.ip_address}"

    def get_device_info(request):
        return request.META.get('HTTP_USER_AGENT', 'unknown-device')

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


# Register UserDevice model for audit logging
auditlog.register(UserDevice)


# EmailOTP Model
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
