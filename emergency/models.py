from django.db import models
#from django.contrib.gis.geos import PointField


# Create your models here.



class EmergencyReport(models.Model):
    message = models.TextField()
    photo = models.ImageField(upload_to='media/emergency_photos/', blank=True)
    scene_description = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Emergency Report: {self.id}"

class Location(models.Model):
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)

    # Foreign key to EmergencyReport if needed
    # report = models.ForeignKey(EmergencyReport, on_delete=models.CASCADE)
