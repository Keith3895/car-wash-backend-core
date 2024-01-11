from rest_framework import serializers
from .models import Vendor, PaymentInformation, KYC

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
    def create(self, validated_data):
        payment_information_data = validated_data.pop('payment_information')
        kyc_data = validated_data.pop('kyc')
        payment_information = PaymentInformation.objects.create(**payment_information_data)
        kyc = KYC.objects.create(**kyc_data)
        vendor = Vendor.objects.create(payment_information=payment_information, kyc=kyc, **validated_data)
        return vendor
    class Meta:
        model = Vendor
        fields = "__all__"