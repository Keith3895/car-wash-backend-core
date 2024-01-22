from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth import get_user_model
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework_gis.serializers import GeoFeatureModelSerializer



from .models import Address

class UserSerializer(UserDetailsSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "first_name", "last_name", "user_type"]


class RegisterSerializer(RegisterSerializer):
    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data["password1"], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        user.user_type = request.data.get("user_type")
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user

class AddressSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Address
        geo_field = 'location'
        fields = "__all__"
        