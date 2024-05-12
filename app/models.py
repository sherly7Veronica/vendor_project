from django.db import models
from django.db.utils import IntegrityError

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            if 'UNIQUE constraint failed: app_vendor.vendor_code' in str(e):
                # Handle the unique constraint violation for vendor_code field
                print("Error: Vendor code must be unique.")
            else:
                # Re-raise the IntegrityError for other cases
                raise e


class PurchaseOrder(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'PENDING'),
        ('COMPLETED', 'COMPLETED'),
        ('CANCELLED', 'CANCELLED'),
    )
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)   
    order_date = models.DateTimeField()   
    delivery_date = models.DateTimeField()  
    items = models.JSONField(null=True, blank=True)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgement_date = models.DateTimeField()

    def __str__(self):
        return self.po_number

class VendorPerformance(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)

    def __str__(self):
        return f"Vendor: {self.vendor}, Date: {self.date}"

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            if 'UNIQUE constraint failed: app_purchaseorder.po_number' in str(e):
                # Handle the unique constraint violation for po_number field
                print("Error: Purchase order number must be unique.")
            else:
                # Re-raise the IntegrityError for other cases
                raise e
