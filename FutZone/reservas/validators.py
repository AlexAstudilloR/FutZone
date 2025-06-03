from django.core.exceptions import ValidationError
from horario.models import HorarioDisponible

class AppointmentValidator:
    dias_es = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    @staticmethod
    def validate(instance):
        # Validación parcial para PATCH (solo estado, por ejemplo)
        required_fields = ['date', 'time_start', 'time_end', 'field']
        if any(getattr(instance, field, None) is None for field in required_fields):
            return

        # Validar orden de horario
        if instance.time_start >= instance.time_end:
            raise ValidationError("La hora de inicio debe ser menor a la hora de fin.")

        # Validar si hay horario disponible
        dia_semana = AppointmentValidator.dias_es[instance.date.weekday()]
        try:
            horario = HorarioDisponible.objects.get(
                cancha=instance.field,
                diaSemana=dia_semana,
                disponible=True
            )
        except HorarioDisponible.DoesNotExist:
            raise ValidationError("No hay un horario disponible para esta cancha en ese día.")

        if not (horario.horaInicio <= instance.time_start and instance.time_end <= horario.horaFin):
            raise ValidationError("La reserva está fuera del horario disponible.")

        # Validar traslape solo si ya hay disponibilidad
        overlap = instance.__class__.objects.filter(
            field=instance.field,
            date=instance.date
        ).exclude(pk=instance.pk).filter(
            time_start__lt=instance.time_end,
            time_end__gt=instance.time_start
        ).exists()

        if overlap:
            raise ValidationError("Esta franja horaria se superpone con otra reserva.")
