from datetime import datetime, date, timedelta
from django.core.exceptions import ValidationError
from horario.models import WeeklySchedule, DateException
from django.db.models import Q

class AppointmentValidator:
    dias_es = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    @staticmethod
    def validate(instance):
        now = datetime.now()

        # Validación para cancelaciones
        if instance.status == 'cancelled':
            if instance._original_status in ['accepted', 'rejected']:
                raise ValidationError("No se puede cancelar una reserva que ya fue aceptada o rechazada.")
            start_datetime = datetime.combine(instance.date, instance.time_start)
            if start_datetime - now < timedelta(hours=1):
                raise ValidationError("Solo puedes cancelar una reserva con al menos 1 hora de anticipación.")
            return  

        # Rechazar reservas pasadas
        if instance.status == 'pending' and instance.date < date.today():
            instance.status = 'rejected'

        if instance.date < date.today() and instance.status != 'rejected':
            raise ValidationError("No se puede reservar en una fecha pasada.")

        required = ['date', 'time_start', 'time_end', 'field']
        if any(getattr(instance, f, None) is None for f in required):
            return  # Faltan datos, detener validación

        # Validar que hora de inicio < hora de fin
        if instance.time_start >= instance.time_end:
            raise ValidationError("La hora de inicio debe ser menor a la hora de fin.")

        # Validar duración mínima (30 minutos)
        start_dt = datetime.combine(instance.date, instance.time_start)
        end_dt = datetime.combine(instance.date, instance.time_end)
        duration = (end_dt - start_dt).total_seconds() / 60
        if duration < 30:
            raise ValidationError("La duración mínima de una reserva debe ser de 30 minutos.")
        
        # Validar que si es hoy, la hora no sea en el pasado
        if instance.date == date.today() and instance.time_start <= now.time():
            raise ValidationError("No se puede reservar en un horario que ya pasó.")

        # Validar excepciones
        weekday = instance.date.weekday()
        dia_nombre = AppointmentValidator.dias_es[weekday]

        exc_qs = DateException.objects.filter(cancha=instance.field, fecha=instance.date)

        cierre_total = exc_qs.filter(cerrado=True).first()
        if cierre_total:
            raise ValidationError(f"No se puede reservar: cerrado ({cierre_total.motivo}).")

        especial = exc_qs.filter(cerrado=False).first()
        if especial:
            if not (especial.hora_apertura <= instance.time_start < instance.time_end <= especial.hora_cierre):
                raise ValidationError("La reserva está fuera del horario especial definido para esa fecha.")

        # Validar horario semanal
        try:
            ws = WeeklySchedule.objects.get(cancha=instance.field, dia=weekday)
        except WeeklySchedule.DoesNotExist:
            raise ValidationError("No hay un horario semanal definido para este día.")

        if not (ws.hora_apertura <= instance.time_start < instance.time_end <= ws.hora_cierre):
            raise ValidationError("La reserva está fuera del horario disponible semanal.")

        # Validar solapamientos, solo con reservas activas
        overlap = instance.__class__.objects.filter(
            field=instance.field,
            date=instance.date,
            status__in=['pending', 'accepted']  # solo reservas activas
        ).exclude(pk=getattr(instance, 'pk', None)).filter(
            time_start__lt=instance.time_end,
            time_end__gt=instance.time_start
        ).exists()

        if overlap:
            raise ValidationError("Esta franja horaria se superpone con otra reserva.")
