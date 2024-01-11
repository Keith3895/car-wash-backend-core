from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from car_wash.apps.vendor.serializations import PaymentInformationSerializer, VendorSerializer


# Create your views here.

class PaymentInformation(APIView):
    
    def get(self, request):
        pass

    def post(self, request):
        serializers = PaymentInformationSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Vendor(APIView):
    
    def get(self, request):
        pass

    def post(self, request):
        serializers = VendorSerializer(data=request.data)
        print(repr(serializers))
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


