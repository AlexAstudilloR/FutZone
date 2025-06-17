from rest_framework import serializers
from .models import Appointment
from .validators import AppointmentValidator
from decimal import Decimal

class AppointmentSerializer(serializers.ModelSerializer):
    valor_pagar = serializers.DecimalField(
        max_digits=6, decimal_places=2, read_only=True
    )
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    field_name = serializers.CharField(source='field.name', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'user', 'user_full_name',
            'field', 'field_name',
            'date', 'time_start', 'time_end',
            'valor_pagar', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'valor_pagar', 'created_at' ,'user']

    def validate(self, data):

        instance = self.instance or Appointment(**data)
        AppointmentValidator.validate(instance)
        return data

    def create(self, validated_data):

        ts = validated_data.get("time_start")
        te = validated_data.get("time_end")
        field = validated_data.get("field")
        if ts and te and field:
            duration = (
                (te.hour - ts.hour) +
                (te.minute - ts.minute) / 60
            )
            validated_data['valor_pagar'] = round(Decimal(duration) * field.price, 2)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        ts = validated_data.get("time_start", instance.time_start)
        te = validated_data.get("time_end", instance.time_end)
        field = validated_data.get("field", instance.field)
        if ts and te and field:
            duration = (
                (te.hour - ts.hour) +
                (te.minute - ts.minute) / 60
            )
            validated_data['valor_pagar'] = round(Decimal(duration) * field.price, 2)
        return super().update(instance, validated_data)
