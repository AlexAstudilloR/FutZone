from rest_framework import serializers
from .models import Appointment
from .validators import AppointmentValidator
from decimal import Decimal

class AppointmentSerializer(serializers.ModelSerializer):
    valor_pagar = serializers.DecimalField(
        max_digits=6, decimal_places=2, read_only=True
    )

    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):
        # Crear instancia temporal para validar
        instance = self.instance or Appointment(**data)

        # Aplicar lógica de validación (traslapes, horarios, etc.)
        AppointmentValidator.validate(instance)

        return data

    def create(self, validated_data):
        # Calcular valor_pagar directamente aquí
        time_start = validated_data.get("time_start")
        time_end = validated_data.get("time_end")
        field = validated_data.get("field")

        if time_start and time_end and field:
            duration = (
                (time_end.hour - time_start.hour) +
                (time_end.minute - time_start.minute) / 60
            )
            validated_data['valor_pagar'] = round(Decimal(duration) * field.price, 2)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Recalcular si se cambian los campos clave
        time_start = validated_data.get("time_start", instance.time_start)
        time_end = validated_data.get("time_end", instance.time_end)
        field = validated_data.get("field", instance.field)

        if time_start and time_end and field:
            duration = (
                (time_end.hour - time_start.hour) +
                (time_end.minute - time_start.minute) / 60
            )
            validated_data['valor_pagar'] = round(Decimal(duration) * field.price, 2)

        return super().update(instance, validated_data)
