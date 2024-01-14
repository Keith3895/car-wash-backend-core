import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator

from car_wash.apps.authentication.models import Address, BaseModel

from storages.backends.gcloud import GoogleCloudStorage

storage = GoogleCloudStorage()

"""
TODO: we should move this to be shared across apps. also we change the name to be more generic.
"""
class VendorDocument(BaseModel):
    document_url = models.CharField(max_length=255, null=True, blank=True)
    document_type = models.CharField(max_length=255, null=True, blank=True)
    document_name = models.CharField(max_length=255, null=True, blank=True)
    vendor = models.ForeignKey(
        "Vendor",
        on_delete=models.CASCADE,
        related_name="vendor_images",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.document_name


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
    gst_certificate = models.OneToOneField(
        VendorDocument,
        on_delete=models.CASCADE,
        related_name="gst_certificate",
        null=True,
        blank=True,
    )
    user_photo = models.OneToOneField(
        VendorDocument,
        on_delete=models.CASCADE,
        related_name="user_photo",
        null=True,
        blank=True,
    )

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
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name


class Upload:
    @staticmethod
    def upload_image(file, filename):
        try:
            target_path = "images/" + uuid.uuid4().hex + filename
            path = storage.save(target_path, file.file)
            return path  # storage.url(path)
        except Exception as e:
            print("Failed to upload!", e)

    @staticmethod
    def upload_pdf(file, filename):
        try:
            target_path = "pdf/" + filename
            path = storage.save(target_path, file.file)
            return path
        except Exception as e:
            print("Failed to upload!")

    @staticmethod
    def get_files(path):
        try:
            return storage.url(path)
        except Exception as e:
            print("Failed to get files!")
