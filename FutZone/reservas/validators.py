from django.core.exceptions import ValidationError
from horario.models import WeeklySchedule, DateException
from django.db.models import Q
from datetime import date

class AppointmentValidator:
    dias_es = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    @staticmethod
    def validate(instance):

        if instance.date < date.today():
            raise ValidationError("No se puede reservar en una fecha pasada.")
        

        required = ['date', 'time_start', 'time_end', 'field']
        if any(getattr(instance, f, None) is None for f in required):
            return
        

        if instance.time_start >= instance.time_end:
            raise ValidationError("La hora de inicio debe ser menor a la hora de fin.")
        
     
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

        

        try:
            ws = WeeklySchedule.objects.get(cancha=instance.field, dia=weekday)
        except WeeklySchedule.DoesNotExist:
            raise ValidationError("No hay un horario semanal definido para este día.")
        
        if ws.cerrado:
            raise ValidationError("Este día la cancha está cerrada.")
        
        if not (ws.hora_apertura <= instance.time_start < instance.time_end <= ws.hora_cierre):
            raise ValidationError("La reserva está fuera del horario disponible semanal.")
        

        overlap = instance.__class__.objects.filter(
            field=instance.field,
            date=instance.date
        ).exclude(pk=getattr(instance, 'pk', None)).filter(
            time_start__lt=instance.time_end,
            time_end__gt=instance.time_start
        ).exists()
        if overlap:
            raise ValidationError("Esta franja horaria se superpone con otra reserva.")
