from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from reservas.models import Appointment
from utils.whatsapp import send_whatsapp_message

ADMIN_NUMBER = "+593979624280"  
@receiver(post_save, sender=Appointment)
def notificar_reserva(sender, instance, created, **kwargs):
    numero = instance.user.cell_phone
    if not numero:
        print("El usuario no tiene número asignado.")
        return

    if created:
        mensaje_usuario = (
            f"¡Tu reserva ha sido registrada!\n\n"
            f"📅 Fecha: {instance.date}\n"
            f"⏰ Hora: {instance.time_start} - {instance.time_end}\n"
            f"🏟️ Cancha: {instance.field.name}\n"
            f"💵 Valor: ${instance.valor_pagar:.2f}\n\n"
            "Realiza el pago escaneando este código QR de Peigo.\n"
            "Cuando esté confirmado, recibirás una notificación ✅"
        )
        mensaje_admin = (
            f"📥 Nueva reserva creada por {instance.user.full_name}.\n"
            f"Fecha: {instance.date}\n"
            f"Hora: {instance.time_start} - {instance.time_end}\n"
            f"Cancha: {instance.field.name}"
            f"Valor a cobrar:{instance.valor_pagar}"
        )
        try:
            sid_user = send_whatsapp_message(numero, mensaje_usuario, media_url=settings.PEIGO_QR_URL)
            sid_admin = send_whatsapp_message(ADMIN_NUMBER, mensaje_admin)
            print("WhatsApp con QR enviado. SID usuario:", sid_user)
            print("Notificación enviada al admin. SID:", sid_admin)
        except Exception as e:
            print("Error enviando mensajes de creación:", e)
        return


    try:
        estado_anterior = instance._original_status
    except Appointment.DoesNotExist:
        print("No se pudo obtener estado anterior.")
        return


    if estado_anterior != 'accepted' and instance.status == 'accepted':
        mensaje_usuario = (
            f"¡Reserva Confirmada!\n\n"
            f"Fecha: {instance.date}\n"
            f"Hora: {instance.time_start} - {instance.time_end}\n"
            f"Cancha: {instance.field.name}\n\n"
            "Gracias por tu pago. ¡Te esperamos!"
        )
        mensaje_admin = (
            f"✅ Reserva ACEPTADA:\n"
            f"Cliente: {instance.user.full_name}\n"
            f"Fecha: {instance.date} | {instance.time_start}-{instance.time_end}\n"
            f"Cancha: {instance.field.name}"
        )
        try:
            sid_user = send_whatsapp_message(numero, mensaje_usuario)
            sid_admin = send_whatsapp_message(ADMIN_NUMBER, mensaje_admin)
            print("Confirmación enviada. SID usuario:", sid_user)
            print("Admin notificado. SID:", sid_admin)
        except Exception as e:
            print("Error enviando confirmación:", e)


    elif estado_anterior != 'rejected' and instance.status == 'rejected':
        mensaje_usuario = (
            "Tu reserva fue rechazada por el administrador.\n"
            "Contacta al personal para más información."
        )
        mensaje_admin = (
            f"❌ Reserva RECHAZADA:\n"
            f"Cliente: {instance.user.full_name}\n"
            f"Fecha: {instance.date} | {instance.time_start}-{instance.time_end}\n"
            f"Cancha: {instance.field.name}"
        )
        try:
            sid_user = send_whatsapp_message(numero, mensaje_usuario)
            sid_admin = send_whatsapp_message(ADMIN_NUMBER, mensaje_admin)
            print("Rechazo enviado. SID usuario:", sid_user)
            print("Admin notificado. SID:", sid_admin)
        except Exception as e:
            print("Error enviando rechazo:", e)
