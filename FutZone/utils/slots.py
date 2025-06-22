from datetime import datetime, timedelta
from horario.models import DateException, WeeklySchedule

def get_open_close(cancha_id, fecha):
    # Verifica excepciones de fecha
    exc = DateException.objects.filter(cancha_id=cancha_id, fecha=fecha).first()
    if exc:
        if exc.cerrado: 
            return None, None
        return (
            datetime.combine(fecha, exc.hora_apertura),
            datetime.combine(fecha, exc.hora_cierre)
        )


    weekday = fecha.weekday()
    sched = WeeklySchedule.objects.filter(cancha_id=cancha_id, dia=weekday).first()
    
    if not sched:
        return None, None  # no hay horario programado para ese día

    return (
        datetime.combine(fecha, sched.hora_apertura),
        datetime.combine(fecha, sched.hora_cierre)
    )


def generate_slots(apertura, cierre, slot_minutes):
    delta = timedelta(minutes=slot_minutes)
    slots = []
    cur = apertura

    while cur + delta <= cierre:
        slots.append({
            "start": cur.time().strftime("%H:%M"),
            "end": (cur + delta).time().strftime("%H:%M")
        })
        cur += delta

    return slots
