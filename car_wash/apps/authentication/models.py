from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.gis.db import models
from car_wash.config import USER_TYPES
import uuid


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    # Custom manager to deal with emails as unique identifiers
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        if not password:
            raise ValueError("The Password must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser, BaseModel):
    USER_TYPE_CHOICES = [(v, k) for k, v in USER_TYPES.items()]

    # Use email as the unique identifier instead of username
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField("email address", unique=True)
    phone = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_JSON(self):
        return {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "user_type": self.user_type,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active
        }


class Customer(models.Model):
    cuid = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile",
    )
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    is_profile_completed = models.BooleanField(default=False, null=True)
    is_account_verified = models.BooleanField(default=False)
    preferred_contact_method = models.CharField(
        max_length=50, choices=[("email", "Email"), ("phone", "Phone")], default="email"
    )
    referral_code = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    location = models.PointField(geography=True, srid=4326, null=True, blank=True)
    address_type = models.CharField(
        max_length=50,
        choices=[("billing", "Billing"), ("shipping", "Shipping"), ("both", "Both")],
        default="both",
    )
    default = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.street}, {self.city}, {self.state}, {self.zip_code}, {self.country}"
        )
