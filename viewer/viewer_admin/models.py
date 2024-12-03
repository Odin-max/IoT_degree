from django.db import models

# Create your models here.


class IotData(models.Model):
    timestamp = models.DateTimeField()
    last_updated = models.DateTimeField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    device_id = models.CharField(unique=True, max_length=255)
    device_type = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=255)
    mac_address = models.CharField(max_length=255)
    connection_status = models.CharField(max_length=50)
    critical_data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iot_data'
