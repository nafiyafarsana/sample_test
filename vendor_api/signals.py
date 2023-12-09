from django.db.models.signals import post_save, post_delete
from .models import PurchaseOrder, Vendor, HistoricalPerformance
from django.utils import timezone

def update_vendor_performance_metrics(sender, instance, **kwargs):
    """
    Signal handler for updating vendor performance metrics on the completion of a purchase order.

    Args:
        sender (class): The model class that sends the signal.
        instance: The instance of the model that triggered the signal.
        kwargs: Additional keyword arguments.

    Returns:
        None
    """
    if instance.status == 'completed':
        instance.vendor.update_performance_metrics()

post_save.connect(update_vendor_performance_metrics, sender=PurchaseOrder)

def update_historical_performance(sender, instance, **kwargs):
    """
    Signal handler for updating historical performance metrics on the completion, successful completion,
    or cancellation of a purchase order.

    Args:
        sender (class): The model class that sends the signal.
        instance: The instance of the model that triggered the signal.
        kwargs: Additional keyword arguments.

    Returns:
        None
    """
    if instance.status in ['completed', 'completed_successfully', 'canceled']:
        historical_performance = HistoricalPerformance(
            vendor=instance.vendor,
            date=timezone.now(),
            on_time_delivery_rate=instance.vendor.on_time_delivery_rate,
            quality_rating_avg=instance.vendor.quality_rating_avg,
            average_response_time=instance.vendor.average_response_time,
            fulfillment_rate=instance.vendor.fulfillment_rate
        )
        historical_performance.save()

post_save.connect(update_historical_performance, sender=PurchaseOrder)

def update_vendor_response_time(sender, instance, created, **kwargs):
    if created or not instance.acknowledgment_date:
        return
    instance.vendor.update_performance_metrics()

post_save.connect(update_vendor_response_time, sender=PurchaseOrder)