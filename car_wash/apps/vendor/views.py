from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from car_wash.apps.vendor.models import Upload
from car_wash.apps.vendor.serializations import PaymentInformationSerializer, VendorDocumentSerializer, VendorSerializer


# Create your views here.

class VendorDocument(APIView):
        def get(self, request):
            # the request params has document path
            redirect = Upload.get_files(request.GET.get("document_path"))
            return HttpResponseRedirect(redirect)
    
        def post(self, request):
            file = request.FILES
            serializers = VendorDocumentSerializer(data=file)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

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
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request):
    #     vendor = Vendor.objects.get(id=request.data["id"])
    #     serializser = VendorSerializer(vendor, data=request.data)
