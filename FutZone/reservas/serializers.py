from rest_framework import serializers
from .models import Appointment
from .validators import AppointmentValidator

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):
        instance = Appointment(**data)
        AppointmentValidator.validate(instance)
        return data
