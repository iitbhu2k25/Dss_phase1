from django.db import models

# raster module 
class RasterVisual(models.Model):
    organisations = models.CharField(max_length=50)
    name = models.CharField(max_length=20,unique=True)
    file_location = models.FileField(upload_to='rasters/')  # Stores file in `MEDIA_ROOT/rasters/`

    def __str__(self):
        return f"{self.name} - {self.organisations}"
    