from django.db import models
from cancha.models import SoccerField

class HorarioFlexible(models.Model):
    TIPO_HORARIO = [
        ('recurrente', 'Recurrente semanal'),
        ('excepcion', 'Excepción por fecha'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_HORARIO, default='recurrente')

    diaSemana = models.CharField(
        max_length=20,
        choices=[
            ('Lunes', 'Lunes'),
            ('Martes', 'Martes'),
            ('Miércoles', 'Miércoles'),
            ('Jueves', 'Jueves'),
            ('Viernes', 'Viernes'),
            ('Sábado', 'Sábado'),
            ('Domingo', 'Domingo'),
        ],
        blank=True, null=True
    )

    fecha = models.DateField(blank=True, null=True)

    horaInicio = models.TimeField(blank=True, null=True)
    horaFin = models.TimeField(blank=True, null=True)

    disponible = models.BooleanField(default=True)
    motivo_bloqueo = models.TextField(blank=True, null=True)

    cancha = models.ForeignKey(
        SoccerField,
        on_delete=models.CASCADE,
        related_name="horarios_flexibles"
    )

    def __str__(self):
        detalle = self.diaSemana if self.tipo == 'recurrente' else str(self.fecha)
        estado = "Disponible" if self.disponible else "No Disponible"
        return f"{self.cancha} - {detalle} ({self.horaInicio} a {self.horaFin}) [{estado}]"
