from django.core.exceptions import ValidationError
from horario.models import HorarioDisponible

class AppointmentValidator:
    dias_es = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    @staticmethod
    def validate(instance):
        # Validar que hora de inicio sea menor que la hora de fin
        if instance.time_start >= instance.time_end:
            raise ValidationError("La hora de inicio debe ser menor a la hora de fin.")

        # Verificar traslape con otras reservas de la misma cancha en la misma fecha
        overlap = instance.__class__.objects.filter(
            field=instance.field,
            date=instance.date
        ).exclude(id=instance.id).filter(
            time_start__lt=instance.time_end,
            time_end__gt=instance.time_start
        ).exists()

        if overlap:
            raise ValidationError("Esta franja horaria se superpone con otra reserva.")

        # Verificar que el horario esté dentro del horario disponible
        dia_semana = AppointmentValidator.dias_es[instance.date.weekday()]
        try:
            disponible = HorarioDisponible.objects.get(
                cancha=instance.field,
                diaSemana=dia_semana,
                disponible=True
            )
        except HorarioDisponible.DoesNotExist:
            raise ValidationError("No hay horario disponible para esta cancha en ese día.")

        if not (disponible.horaInicio <= instance.time_start and instance.time_end <= disponible.horaFin):
            raise ValidationError("La reserva está fuera del horario disponible.")
