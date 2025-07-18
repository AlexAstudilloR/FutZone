from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from reservas.models import Appointment
from utils.whatsapp import send_whatsapp_message
from profiles.models import ProfileModel

ADMIN_NUMBER = "+593979624280"

@receiver(post_save, sender=Appointment)
def notificar_reserva(sender, instance, created, **kwargs):
    numero = instance.user.cell_phone
    if not numero:
        print("El usuario no tiene número asignado.")
        return

    admin_profile = ProfileModel.objects.filter(is_admin=True).order_by('-updated_at').first()
    qr_url = None

    if admin_profile and admin_profile.payment_qr:
        qr_path = admin_profile.payment_qr.name
        if qr_path:
            qr_url = f"https://a6bf8005bf81.ngrok-free.app/{qr_path}"
            print(f"QR URL construida desde DB: {qr_url}")

    if created:
        mensaje_usuario = (
            f"¡Tu reserva ha sido registrada!\n\n"
            f"📅 Fecha: {instance.date}\n"
            f"⏰ Hora: {instance.time_start} - {instance.time_end}\n"
            f"🏟️ Cancha: {instance.field.name}\n"
            f"💵 Valor: ${instance.valor_pagar:.2f}\n\n"
        )
        
        if qr_url:
            mensaje_usuario += (
                "Realiza el pago escaneando este código QR de Peigo.\n"
                "Cuando esté confirmado, recibirás una notificación ✅\n"
                "En caso de algún inconveniente con el pago comunicate a 097 962 4280"
            )
        else:
            mensaje_usuario += (
                "Para realizar el pago, comunícate al 097 962 4280\n"
                "Cuando esté confirmado, recibirás una notificación ✅"
            )
        
        mensaje_admin = (
            f"📥 Nueva reserva creada por {instance.user.full_name}.\n"
            f"Fecha: {instance.date}\n"
            f"Hora: {instance.time_start} - {instance.time_end}\n"
            f"Cancha: {instance.field.name}\n"
            f"Valor a cobrar: {instance.valor_pagar}"
        )
        
        try:
            if qr_url:
                sid_user = send_whatsapp_message(numero, mensaje_usuario, media_url=qr_url)
                print("WhatsApp con QR enviado. SID usuario:", sid_user)
            else:
                sid_user = send_whatsapp_message(numero, mensaje_usuario)
                print("WhatsApp SIN QR enviado. SID usuario:", sid_user)
                
            sid_admin = send_whatsapp_message(ADMIN_NUMBER, mensaje_admin, media_url=qr_url)
            print("Notificación enviada al admin. SID:", sid_admin)
        except Exception as e:
            print("Error enviando mensajes de creación:", e)
        return

    try:
        estado_anterior = instance._original_status
    except AttributeError:
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

    elif estado_anterior != 'cancelled' and instance.status == 'cancelled':
        mensaje_usuario = (
            "Tu reserva ha sido cancelada exitosamente.\n"
            "Si fue un error, puedes volver a reservar desde la aplicación."
        )
        mensaje_admin = (
            f"⚠️ RESERVA CANCELADA por el cliente:\n"
            f"Cliente: {instance.user.full_name}\n"
            f"Fecha: {instance.date} | {instance.time_start}-{instance.time_end}\n"
            f"Cancha: {instance.field.name}"
        )
        try:
            sid_user = send_whatsapp_message(numero, mensaje_usuario)
            sid_admin = send_whatsapp_message(ADMIN_NUMBER, mensaje_admin)
            print("Cancelación enviada. SID usuario:", sid_user)
            print("Admin notificado de cancelación. SID:", sid_admin)
        except Exception as e:
            print("Error enviando cancelación:", e)