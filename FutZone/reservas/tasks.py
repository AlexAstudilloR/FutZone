# appointments/tasks.py
from celery import shared_task
from datetime import date
from .models import Appointment
from utils.whatsapp import send_whatsapp_message 
@shared_task
def rechazar_reservas_vencidas_diario():
    Appointment.objects.filter(
        status='pending',
        date__lt=date.today()
    ).update(status='rejected')


@shared_task
def recordatorio_reservas_pendientes():
    count = Appointment.objects.filter(status='pending').count()

    if count > 0:
        mensaje = f"📢 Tienes {count} reserva(s) pendientes por revisar en FutZone. Ingresa al panel para gestionarlas."
        send_whatsapp_message(
            to_number="0979624280",  # Reemplaza con el número real del administrador
            body=mensaje
        )