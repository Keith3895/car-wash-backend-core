from django.urls import path
from . import views


urlpatterns = [
    path('', views.Vendor.as_view()),
    path('payment-information/', views.PaymentInformation.as_view()),
    path('vendor-document/', views.VendorDocument.as_view()),
]
