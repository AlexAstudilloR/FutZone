def normalizar_numero(numero):
    numero = numero.strip()
    if numero.startswith("0"):
       
        return f"+593{numero[1:]}"
    elif numero.startswith("+"):
        return numero  
    else:
        return f"+593{numero}" 

def send_whatsapp_message(to_number, body, media_url=None):
    from twilio.rest import Client
    from django.conf import settings

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    numero_normalizado = f"whatsapp:{normalizar_numero(to_number)}"

    message_data = {
        "from_": settings.TWILIO_WHATSAPP_NUMBER,
        "to": numero_normalizado,
        "body": body
    }

    if media_url:
        message_data["media_url"] = [media_url]

    message = client.messages.create(**message_data)
    return message.sid
