from django.db import models

class KioskLocations(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    status = models.CharField(max_length=1, default='1')  # Add the new field
    created_at = models.DateTimeField()


    class Meta:
        managed = False  # Ensure Django doesn't manage migrations for this table
        db_table = 'kiosk_locations'

