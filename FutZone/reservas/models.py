from django.db import models
from django.core.exceptions import ValidationError
#from profiles.models import ProfileModel   #ACTIVAR NUEVAMENTE
from django.contrib.auth.models import User  # modelo de Django por defecto
from cancha.models import SoccerField  


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    #user = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, related_name='appointments')    #ACTIVAR CUANDO SE TRABAJE CON SUPABASE
    user = models.ForeignKey(User, on_delete=models.CASCADE)#Cuando se use supabase esta linea se debe borrar.
    field = models.ForeignKey(SoccerField, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()

    time_start = models.TimeField()
    time_end = models.TimeField()
    valor_pagar = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"{self.user} - {self.field} - {self.date} ({self.time_start} - {self.time_end})"
