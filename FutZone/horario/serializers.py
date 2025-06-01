from rest_framework import serializers
from .models import HorarioDisponible  # Ya no importamos Cancha aquí

class HorarioDisponibleSerializer(serializers.ModelSerializer):
    cancha_info = serializers.StringRelatedField(source='cancha', read_only=True)

    class Meta:
        model = HorarioDisponible
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Si está disponible, eliminamos el campo "motivo_bloqueo"
        if data['disponible'] is True:
            data.pop('motivo_bloqueo', None)
        return data


    def validate(self, data):
        dia = data['diaSemana']
        hora_inicio = data['horaInicio']
        hora_fin = data['horaFin']
        cancha = data['cancha']
        disponible = data.get('disponible', True)
        motivo_bloqueo = data.get('motivo_bloqueo', '')

        if hora_inicio >= hora_fin:
            raise serializers.ValidationError("La hora de inicio debe ser menor a la hora fin.")

        if disponible:
            traslape = HorarioDisponible.objects.filter(
                diaSemana=dia,
                cancha=cancha
            ).exclude(id=self.instance.id if self.instance else None).filter(
                horaInicio__lt=hora_fin,
                horaFin__gt=hora_inicio
            ).exists()

            if traslape:
                raise serializers.ValidationError("El horario se traslapa con uno ya existente.")

        if not disponible and not motivo_bloqueo:
            raise serializers.ValidationError("Debe especificar un motivo si el horario está bloqueado.")

        return data
