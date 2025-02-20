from django.db import models

class Order(models.Model):
    PAGE_TYPE_CHOICES = [
        ('A3', 'A3'),
        ('A4', 'A4'),
    ]

    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Printed', 'Printed'),
        ('Refunded', 'Refunded'),
    ]

    order_id = models.AutoField(primary_key=True)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pages_selected = models.IntegerField(default=0)
    is_singleside = models.IntegerField(default=True)
    is_color = models.IntegerField(default=False)
    no_copy = models.IntegerField(default=1)
    page_type = models.CharField(max_length=2, choices=PAGE_TYPE_CHOICES)
    recipt_file = models.CharField(max_length=255, blank=True, null=True)
    date_paid = models.DateTimeField(null=True, blank=True)
    date_printed = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    trx_id = models.CharField(max_length=100, blank=True, null=True)
    kiosk_location_name = models.CharField(max_length=255, default='', blank=True)
    printer_name = models.CharField(max_length=255, default='', blank=True)
    printer_id = models.CharField(max_length=11, default='', blank=True)
    kiosk_id = models.IntegerField(default=0, blank=True, null=True)
    mobile_device_id = models.CharField(max_length=100, blank=True, null=True)
    file_name=models.TextField()
    order_status = models.CharField(
        max_length=10,
        choices=ORDER_STATUS_CHOICES,
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders' 