from django.db import models


# Planteo del modelo de cancha (Es posible que sea necesario modificar a futuro)
class SoccerField(models.Model):
    name= models.CharField(max_length=20)
    field_type= models.CharField(max_length=20)
    price= models.DecimalField(max_digits=8, decimal_places=2)
    available=models.BooleanField(default=True)
    image=models.ImageField(upload_to='soccer_fields/', null=True, blank=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.field_type}"