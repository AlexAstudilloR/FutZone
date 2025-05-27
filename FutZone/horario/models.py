from django.db import models
from django.core.exceptions import ValidationError

class Cancha(models.Model):
    dimensiones = models.CharField(max_length=20)
    tarifa = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.dimensiones} - ${self.tarifa}"


class HorarioDisponible(models.Model):
    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    diaSemana = models.CharField(max_length=20, choices=DIAS_SEMANA)
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    disponible = models.BooleanField(default=True)
    motivo_bloqueo = models.TextField(blank=True, null=True)  #Agregado recientemente
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, related_name="horarios")

    def __str__(self):
        estado = "Disponible" if self.disponible else "No Disponible"
        return f"{self.cancha} - {self.diaSemana} de {self.horaInicio} a {self.horaFin} ({estado})"

    def clean(self):
        if self.horaInicio >= self.horaFin:
            raise ValidationError("La hora de inicio debe ser anterior a la hora fin.")
            
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
