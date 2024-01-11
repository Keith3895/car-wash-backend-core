from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


def email_confirm_redirect(request, key):
    return HttpResponseRedirect(f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/")


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )


@api_view(["Patch"])
@permission_classes([IsAuthenticated])
def user_details(request):
    user = get_user_model().objects.get(id=request.user.pk)
    user.first_name = request.data.get("first_name")
    user.last_name = request.data.get("last_name")
    user.phone = request.data.get("phone")
    user.user_type = request.data.get("user_type")
    user.save()
    return JsonResponse(user.get_JSON(), status=status.HTTP_200_OK)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "{settings.HOST_URL}/api/auth/google"
    client_class = OAuth2Client
