import os
from datetime import datetime
from django.db import models

def custom_field_image_upload(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    name = instance.name.replace(' ', '_').lower()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f'soccer_fields/{name}_{timestamp}{ext}'

class SoccerField(models.Model):
    name = models.CharField(max_length=20)
    field_type = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to=custom_field_image_upload, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.field_type}"
