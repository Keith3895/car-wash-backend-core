from rest_framework import serializers
from .models import Upload, Vendor, PaymentInformation, KYC, VendorDocument


class VendorDocumentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def create_vendor_document(self, file, filename):
        if not file:
            raise ValueError("No file provided")
        if not filename:
            raise ValueError("No filename provided")
        if not file.content_type:
            raise ValueError("No content type provided")
        if file.content_type.startswith("image"):
            document_url = Upload.upload_image(file, filename)
        elif file.content_type.startswith("application/pdf"):
            document_url = Upload.upload_pdf(file, filename)
        document_type = file.content_type
        document_name = filename

        return {
            "document_url": document_url,
            "document_type": document_type,
            "document_name": document_name,
        }

    def validate(self, validated_data):
        if not validated_data:
            validated_data = self.create_vendor_document(
                self.initial_data["file"], self.initial_data["file"].name
            )
        return validated_data

    def create(self, validated_data):
        vendor_document = VendorDocument.objects.create(**validated_data)
        return vendor_document

    def update(self, instance, validated_data):
        instance.document_url = validated_data.get(
            "document_url", instance.document_url
        )
        instance.document_type = validated_data.get(
            "document_type", instance.document_type
        )
        instance.document_name = validated_data.get(
            "document_name", instance.document_name
        )
        instance.vendor = validated_data.get("vendor", instance.vendor)
        instance.save()
        return instance

    class Meta:
        model = VendorDocument
        fields = "__all__"


class PaymentInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInformation
        fields = "__all__"


class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = "__all__"


class VendorSerializer(serializers.ModelSerializer):
    payment_information = PaymentInformationSerializer()
    kyc = KYCSerializer()
    vendor_images = VendorDocumentSerializer(many=True)

    def create(self, validated_data):
        payment_information_data = validated_data.pop("payment_information")
        kyc_data = validated_data.pop("kyc")
        payment_information = PaymentInformation.objects.create(
            **payment_information_data
        )
        kyc = KYC.objects.create(**kyc_data)
        vendor_images_data = self.initial_data.pop("vendor_images")
        validated_data.pop("vendor_images")
        vendor = Vendor.objects.create(
            payment_information=payment_information, kyc=kyc, **validated_data
        )

        for vendor_image_data in vendor_images_data:
            VendorDocument.objects.filter(id=vendor_image_data.get("id")).update(
                vendor=vendor
            )
        return vendor

    class Meta:
        model = Vendor
        fields = "__all__"

