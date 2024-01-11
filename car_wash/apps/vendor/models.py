from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator

from car_wash.apps.authentication.models import Address, BaseModel


# Create your models here.
class PaymentInformation(BaseModel):
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    bank_account_number = models.CharField(max_length=255, null=True, blank=True)
    bank_ifsc_code = models.CharField(
        max_length=11, null=True, blank=True, validators=[MinLengthValidator(11)]
    )
    card_number = models.CharField(
        max_length=16, null=True, blank=True, validators=[MinLengthValidator(16)]
    )
    card_expiry_date = models.DateField(null=True, blank=True)
    card_cvv = models.CharField(
        max_length=3, null=True, blank=True, validators=[MinLengthValidator(3)]
    )
    upi_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.payment_method


class KYC(BaseModel):
    pan_number = models.CharField(
        max_length=10, null=True, blank=True, validators=[MinLengthValidator(10)]
    )
    aadhar_number = models.CharField(
        max_length=12, null=True, blank=True, validators=[MinLengthValidator(12)]
    )
    gst_number = models.CharField(
        max_length=15, null=True, blank=True, validators=[MinLengthValidator(15)]
    )
    gst_certificate_image = models.CharField(max_length=255, null=True, blank=True)
    other_document_number = models.CharField(max_length=255, null=True, blank=True)
    other_document_image = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.vendor.company_name


class Vendor(BaseModel):
    uid = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vendor_profile",
    )
    company_name = models.CharField(max_length=255)
    is_profile_completed = models.BooleanField(default=False, null=True)
    is_account_verified = models.BooleanField(default=False)
    preferred_contact_method = models.CharField(
        max_length=50, choices=[("email", "Email"), ("phone", "Phone")], default="email"
    )
    vendor_address = models.OneToOneField(
        Address, on_delete=models.CASCADE, related_name="vendor", null=True, blank=True
    )
    payment_information = models.OneToOneField(
        PaymentInformation,
        on_delete=models.CASCADE,
        related_name="payment_information",
        null=True,
        blank=True,
    )
    kyc = models.OneToOneField(
        KYC, on_delete=models.CASCADE, related_name="kyc", null=True, blank=True
    )

    def __str__(self):
        return self.company_name
