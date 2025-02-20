from django.db import models
class KioskPrinter(models.Model):
    id = models.AutoField(primary_key=True)
    location_id = models.IntegerField()  # Foreign key relation isn't enforced here since the table already exists
    printer_no = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    A3tray= models.IntegerField()
    status = models.CharField(max_length=1, default='1')
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'kiosk_printer' 