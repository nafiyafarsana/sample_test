from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=255, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    def update_performance_metrics(self):
        # Calculate on-time delivery rate
        completed_pos = PurchaseOrder.objects.filter(vendor=self, status='completed').order_by('issue_date')
        on_time_pos = [po for po in completed_pos if po.delivery_date >= po.acknowledgment_date or po.acknowledgment_date is None]
        self.on_time_delivery_rate = len(on_time_pos) / len(completed_pos) if len(completed_pos) > 0 else 0.0

        # Calculate quality rating average
        quality_ratings = [po.quality_rating for po in completed_pos if po.quality_rating is not None]
        self.quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if len(quality_ratings) > 0 else 0.0

        # Calculate average response time
        acknowledged_pos = PurchaseOrder.objects.filter(vendor=self, acknowledgment_date__isnull=False)
        response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in acknowledged_pos]
        self.average_response_time = sum(response_times) / len(response_times) if len(response_times) > 0 else 0.0
        
        # Calculate fulfillment rate
        fulfilled_pos = completed_pos.filter(status__in=['completed', 'completed_successfully'])
        self.fulfillment_rate = len(fulfilled_pos) / len(completed_pos) if len(completed_pos) > 0 else 0.0

        self.save()


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=255, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=255)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return f"Historical Performance for Vendor {self.vendor.name} on {self.date}"