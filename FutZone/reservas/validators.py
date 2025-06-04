from django.core.exceptions import ValidationError
from cancha.models import SoccerField
from horario.models import HorarioFlexible
from django.db.models import Q

class AppointmentValidator:
    dias_es = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    @staticmethod
    def validate(instance):
        required_fields = ['date', 'time_start', 'time_end', 'field']
        if any(getattr(instance, field, None) is None for field in required_fields):
            return

        if instance.time_start >= instance.time_end:
            raise ValidationError("La hora de inicio debe ser menor a la hora de fin.")

        dia_semana = AppointmentValidator.dias_es[instance.date.weekday()]

        # 🔒 Bloqueo por horario flexible
        bloqueado = HorarioFlexible.objects.filter(
            cancha=instance.field,
            disponible=False,
        ).filter(
            Q(tipo='recurrente', diaSemana=dia_semana) |
            Q(tipo='excepcion', fecha=instance.date)
        ).filter(
            horaInicio__lt=instance.time_end,
            horaFin__gt=instance.time_start
        ).first()

        if bloqueado:
            raise ValidationError(f"No se puede reservar en este horario. Motivo: {bloqueado.motivo_bloqueo}"
            )

        # ✅ Verificar disponibilidad
        try:
            horario = HorarioFlexible.objects.get(
                cancha=instance.field,
                disponible=True,
                tipo='recurrente',
                diaSemana=dia_semana
            )
        except HorarioFlexible.DoesNotExist:
            raise ValidationError("No hay un horario disponible definido para este día.")

        if not (horario.horaInicio <= instance.time_start < instance.time_end <= horario.horaFin):
            raise ValidationError("La reserva está fuera del horario disponible.")

        # 🔁 Verificar traslape con otras reservas
        overlap = instance.__class__.objects.filter(
            field=instance.field,
            date=instance.date,
        ).exclude(pk=instance.pk).filter(
            time_start__lt=instance.time_end,
            time_end__gt=instance.time_start
        ).exists()

        if overlap:
            raise ValidationError("Esta franja horaria se superpone con otra reserva.")

