from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import (
        VendorSerializer,
        PurchaseOrderSerializer,
        HistoricalPerformanceSerializer,
        MyTokenObtainPairSerializer,
        PurchaseOrderAcknowledgeSerializer,
)
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


# Create your views here.

class VendorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing vendors.

    Attributes:
    - queryset (QuerySet): The set of all vendors.
    - serializer_class (Serializer): The serializer class for vendors.
    - permission_classes (list): The list of permission classes applied to the view.

    Methods:
    - list(request): Retrieve and return a list of all vendors.
    - create(request): Create and return a new vendor instance.
    - retrieve(request, pk): Retrieve and return the details of a specific vendor.
    - update(request, pk): Update and return the details of an existing vendor.
    - partial_update(request, pk): Partially update and return the details of an existing vendor.
    - destroy(request, pk): Delete an existing vendor.

    Raises:
    - PermissionDenied: Raised when a user tries to perform an action without the necessary permissions.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing purchase orders.

    Attributes:
    - queryset (QuerySet): The set of all purchase orders.
    - serializer_class (Serializer): The serializer class for purchase orders.
    - permission_classes (list): The list of permission classes applied to the view.

    Methods:
    - get_queryset(): Retrieve the queryset filtered by the authenticated user's vendor.
    - acknowledge(request, pk): Acknowledge a purchase order by updating acknowledgment details.

    Actions:
    - acknowledge: Custom action for acknowledging a purchase order.

    Raises:
    - ObjectDoesNotExist: Raised when the requested purchase order is not found.
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'po_number'  
    lookup_url_kwarg = 'pk'
    
    def get_queryset(self):
        """Retrieve the queryset filtered by the authenticated user's vendor."""
        vendor = self.request.user.vendor
        return self.queryset.filter(vendor=vendor)

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """
        Acknowledge a purchase order by updating acknowledgment details.

        Args:
        - request (HttpRequest): The HTTP request object.
        - pk (str): The primary key of the purchase order to acknowledge.

        Returns:
        - Response: The HTTP response indicating the acknowledgment status.

        Raises:
        - ObjectDoesNotExist: Raised when the requested purchase order is not found.
        """
        try:
            purchase_order = self.get_object()
            
            if purchase_order.acknowledgment_date:
                return Response({'detail': 'Purchase order already acknowledged.'}, status=status.HTTP_400_BAD_REQUEST)

            # Update acknowledgment details
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()

            # Trigger the recalculation of average_response_time for the vendor
            purchase_order.vendor.update_performance_metrics()

            # Provide a message in the response body
            return Response({'detail': 'Purchase order acknowledged successfully.'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

class VendorPerformanceView(viewsets.ViewSet):
    """
    ViewSet for retrieving performance metrics of a vendor.

    Attributes:
    - queryset (QuerySet): The set of all vendors.
    - serializer_class (Serializer): The serializer class for vendors.

    Methods:
    - get(request, pk): Retrieve and return the performance metrics of a vendor.

    Raises:
    - ObjectDoesNotExist: Raised when the requested vendor is not found.
    - Exception: Raised for unexpected errors during view execution.
    """
    def get(self, request, pk=None):
        """
        Retrieve and return the performance metrics of a vendor.

        Args:
        - request (HttpRequest): The HTTP request object.
        - pk (int): The primary key of the vendor to retrieve metrics for.

        Returns:
        - Response: The HTTP response containing the vendor's performance metrics.

        Raises:
        - ObjectDoesNotExist: Raised when the requested vendor is not found.
        - Exception: Raised for unexpected errors during view execution.
        """
        try:
            vendor = Vendor.objects.get(pk=pk)
            vendor.update_performance_metrics()  # Ensure metrics are up-to-date
            performance_metrics = {
                'on_time_delivery_rate': vendor.on_time_delivery_rate,
                'quality_rating_avg': vendor.quality_rating_avg,
                'average_response_time': vendor.average_response_time,
                'fulfillment_rate': vendor.fulfillment_rate
            }
            return Response(performance_metrics, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': 'Vendor not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f'Error in VendorPerformanceView: {str(e)}')
            return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HistoricalPerformanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing historical performance records.

    Attributes:
    - queryset (QuerySet): The set of all historical performance records.
    - serializer_class (Serializer): The serializer class for historical performance records.

    Methods:
    - list(request): Retrieve and return a list of all historical performance records.
    - create(request): Create and return a new historical performance record instance.
    - retrieve(request, pk): Retrieve and return the details of a specific historical performance record.
    - update(request, pk): Update and return the details of an existing historical performance record.
    - partial_update(request, pk): Partially update and return the details of an existing historical performance record.
    - destroy(request, pk): Delete an existing historical performance record.

    Raises:
    - PermissionDenied: Raised when a user tries to perform an action without the necessary permissions.
    """
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
    
    
class MyTokenObtainPairView(TokenObtainPairView):
    """
    Token obtain view for obtaining access and refresh tokens.

    Attributes:
    - serializer_class (Serializer): The serializer class for obtaining access and refresh tokens.

    Methods:
    - post(request): Obtain access and refresh tokens for user authentication.

    Raises:
    - APIException: Raised for various API-related errors.
    """
    serializer_class = MyTokenObtainPairSerializer
    
class MyTokenRefreshView(TokenRefreshView):
    """
    Token refresh view for obtaining a new access token using a valid refresh token.

    Attributes:
    - serializer_class (Serializer): The serializer class for obtaining a new access token.

    Methods:
    - post(request): Obtain a new access token using a valid refresh token.

    Raises:
    - APIException: Raised for various API-related errors.
    """
    serializer_class = MyTokenObtainPairSerializer