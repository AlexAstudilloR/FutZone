from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from reservas.models import Appointment
from utils.whatsapp import send_whatsapp_message

@receiver(post_save, sender=Appointment)
def notificar_reserva(sender, instance, created, **kwargs):
    numero = instance.user.cell_phone
    if not numero:
        print("⚠️ El usuario no tiene número asignado.")
        return


    if created:
        mensaje = (
            "📢 ¡Tu reserva ha sido registrada!\n\n"
            "Realiza el pago escaneando este código QR de Peigo.\n"
            "Cuando esté confirmado, recibirás una notificación ✅"
        )
        try:
            sid = send_whatsapp_message(numero, mensaje, media_url=settings.PEIGO_QR_URL)
            print("✅ WhatsApp con QR enviado. SID:", sid)
        except Exception as e:
            print("❌ Error enviando QR:", e)
        return

    # ✅ 2. Cuando el estado cambia a 'accepted'
    try:
        estado_anterior = Appointment.objects.get(pk=instance.pk).status
    except Appointment.DoesNotExist:
        print("⚠️ No se pudo obtener estado anterior.")
        return

    if estado_anterior != 'accepted' and instance.status == 'accepted':
        mensaje = (
            f"✅ ¡Reserva Confirmada!\n\n"
            f"📅 Fecha: {instance.date}\n"
            f"🕒 Hora: {instance.time_start} - {instance.time_end}\n"
            f"⚽ Cancha: {instance.field.name}\n\n"
            "Gracias por tu pago. ¡Te esperamos!"
        )
        try:
            sid = send_whatsapp_message(numero, mensaje)
            print("✅ WhatsApp de confirmación enviado. SID:", sid)
        except Exception as e:
            print("❌ Error enviando confirmación:", e)

    # 🟠 3. Si luego quieres manejar cambios a 'rejected', lo puedes agregar así:
    elif estado_anterior != 'rejected' and instance.status == 'rejected':
        mensaje = (
            "❌ Tu reserva fue rechazada por el administrador.\n"
            "Contacta al personal para más información."
        )
        try:
            sid = send_whatsapp_message(numero, mensaje)
            print("⚠️ WhatsApp de rechazo enviado. SID:", sid)
        except Exception as e:
            print("❌ Error enviando rechazo:", e)
