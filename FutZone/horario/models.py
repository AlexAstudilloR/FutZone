from django.db import models
from cancha.models import SoccerField

class WeeklySchedule(models.Model):
    DIA_CHOICES = [
        (0, "Lunes"),
        (1, "Martes"),
        (2, "Miércoles"),
        (3, "Jueves"),
        (4, "Viernes"),
        (5, "Sábado"),
        (6, "Domingo"),
    ]

    cancha = models.ForeignKey(
        SoccerField, on_delete=models.CASCADE, related_name="weekly_schedules"
    )
    dia = models.IntegerField(choices=DIA_CHOICES)
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()
    cerrado = models.BooleanField(default=False)

    class Meta:
        unique_together = ("cancha", "dia")
        ordering = ["dia"]

    def __str__(self):
        if self.cerrado:
            return f"{self.get_dia_display()}: Cerrado"
        return f"{self.get_dia_display()} {self.hora_apertura}–{self.hora_cierre}"
    
class DateException(models.Model):
    cancha = models.ForeignKey(
        SoccerField, on_delete=models.CASCADE, related_name="date_exceptions"
    )
    fecha = models.DateField()
    hora_apertura = models.TimeField(null=True, blank=True)
    hora_cierre = models.TimeField(null=True, blank=True)
    cerrado = models.BooleanField(default=True)
    motivo = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ("cancha", "fecha")
        ordering = ["-fecha"]

    def __str__(self):
        if self.cerrado:
            return f"{self.fecha}: Cerrado ({self.motivo})"
        return f"{self.fecha} {self.hora_apertura}–{self.hora_cierre}"