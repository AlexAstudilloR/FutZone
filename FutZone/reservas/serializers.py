from rest_framework import serializers
from .models import Appointment
from .validators import AppointmentValidator

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):
        # Crear una instancia temporal o usar la existente (PUT)
        instance = self.instance or Appointment()

        # Actualizar los atributos con los nuevos datos (para edición)
        for attr, value in data.items():
            setattr(instance, attr, value)

        # Validar solo si los campos esenciales están presentes
        AppointmentValidator.validate(instance)
        return data
