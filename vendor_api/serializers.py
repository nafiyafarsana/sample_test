from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Vendor model.

    Attributes:
        Meta: A class containing metadata about the serializer.
            model (class): The model class associated with the serializer.
            fields (tuple): A tuple of fields to include in the serialized output.
    """
    class Meta:
        model = Vendor
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the PurchaseOrder model.

    Attributes:
        Meta: A class containing metadata about the serializer.
            model (class): The model class associated with the serializer.
            fields (tuple): A tuple of fields to include in the serialized output.
    """
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    """
    Serializer for the HistoricalPerformance model.

    Attributes:
        Meta: A class containing metadata about the serializer.
            model (class): The model class associated with the serializer.
            fields (tuple): A tuple of fields to include in the serialized output.
    """
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'


class PurchaseOrderAcknowledgeSerializer(serializers.Serializer):
    """
    Serializer for acknowledging a purchase order.

    Attributes:
    - acknowledgment_notes (str, optional): Additional notes or comments for the acknowledgment.
      Max length is 255 characters.
    """
    acknowledgment_notes = serializers.CharField(max_length=255, required=False)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer.

    This serializer extends the TokenObtainPairSerializer provided by the
    rest_framework_simplejwt library.

    No additional attributes or methods are added. It's intended to be used as
    a placeholder for any potential future customization.
    """
    pass
