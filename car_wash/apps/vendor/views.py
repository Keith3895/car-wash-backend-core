from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from car_wash.apps.vendor.models import Upload
from car_wash.apps.vendor.serializations import PaymentInformationSerializer, VendorDocumentSerializer, VendorSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import Vendor as VendorModel

# Create your views here.
@permission_classes([IsAuthenticated])
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

@permission_classes([IsAuthenticated])
class PaymentInformation(APIView):
    
    def get(self, request):
        pass

    def post(self, request):
        serializers = PaymentInformationSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])    
class Vendor(APIView):
    
    def get(self, request):
        
        # Get query parameters
        # company_name = request.query_params.get('company_name', None)

        # Get all vendors or filter based on query parameters
        if request.user.id is not None:
            vendors = VendorModel.objects.filter(uid=request.user.id)

        # Serialize the vendors
        serializer = VendorSerializer(vendors, many=True)

        # Return the serialized vendors
        return Response(serializer.data)

    def post(self, request):
        serializers = VendorSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request):
    #     vendor = Vendor.objects.get(id=request.data["id"])
    #     serializser = VendorSerializer(vendor, data=request.data)
