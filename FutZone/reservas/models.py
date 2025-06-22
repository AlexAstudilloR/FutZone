from django.db import models
from django.core.exceptions import ValidationError
from profiles.models import ProfileModel   
from cancha.models import SoccerField  


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, related_name='appointments')   
  
    field = models.ForeignKey(SoccerField, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()

    time_start = models.TimeField()
    time_end = models.TimeField()
    valor_pagar = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_status = self.status
    def __str__(self):
        return f"{self.user} - {self.field} - {self.date} ({self.time_start} - {self.time_end}-{self.valor_pagar}"
