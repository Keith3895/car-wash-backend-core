# Generated by Django 4.2.8 on 2024-01-14 07:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0002_delete_vendor'),
    ]

    operations = [
        migrations.CreateModel(
            name='KYC',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pan_number', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.MinLengthValidator(10)])),
                ('aadhar_number', models.CharField(blank=True, max_length=12, null=True, validators=[django.core.validators.MinLengthValidator(12)])),
                ('gst_number', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.MinLengthValidator(15)])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentInformation',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bank_name', models.CharField(blank=True, max_length=255, null=True)),
                ('bank_account_number', models.CharField(blank=True, max_length=255, null=True)),
                ('bank_ifsc_code', models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.MinLengthValidator(11)])),
                ('card_number', models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.MinLengthValidator(16)])),
                ('card_expiry_date', models.DateField(blank=True, null=True)),
                ('card_cvv', models.CharField(blank=True, max_length=3, null=True, validators=[django.core.validators.MinLengthValidator(3)])),
                ('upi_id', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=255)),
                ('is_profile_completed', models.BooleanField(default=False, null=True)),
                ('is_account_verified', models.BooleanField(default=False)),
                ('preferred_contact_method', models.CharField(choices=[('email', 'Email'), ('phone', 'Phone')], default='email', max_length=50)),
                ('is_active', models.BooleanField(default=False)),
                ('kyc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kyc', to='vendor.kyc')),
                ('payment_information', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_information', to='vendor.paymentinformation')),
                ('uid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_profile', to=settings.AUTH_USER_MODEL)),
                ('vendor_address', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to='authentication.address')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VendorDocument',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('document_url', models.CharField(blank=True, max_length=255, null=True)),
                ('document_type', models.CharField(blank=True, max_length=255, null=True)),
                ('document_name', models.CharField(blank=True, max_length=255, null=True)),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_images', to='vendor.vendor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='kyc',
            name='gst_certificate',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gst_certificate', to='vendor.vendordocument'),
        ),
        migrations.AddField(
            model_name='kyc',
            name='user_photo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_photo', to='vendor.vendordocument'),
        ),
    ]
