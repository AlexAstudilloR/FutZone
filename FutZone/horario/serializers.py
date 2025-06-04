from rest_framework import serializers
from .models import HorarioFlexible

class HorarioFlexibleSerializer(serializers.ModelSerializer):
    cancha_info = serializers.StringRelatedField(source='cancha', read_only=True)

    class Meta:
        model = HorarioFlexible
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['disponible']:
            data.pop('motivo_bloqueo', None)
            data.pop('fecha', None)
        return data

    def validate(self, data):
        instance_data = {**data}
        if self.instance:
            for field in self.fields:
                if field not in instance_data:
                    instance_data[field] = getattr(self.instance, field, None)

        tipo = instance_data.get('tipo', 'recurrente')
        dia = instance_data.get('diaSemana')
        fecha = instance_data.get('fecha')
        hora_inicio = instance_data.get('horaInicio')
        hora_fin = instance_data.get('horaFin')
        cancha = instance_data.get('cancha')
        disponible = instance_data.get('disponible', True)
        motivo_bloqueo = instance_data.get('motivo_bloqueo', '')

        # 1. Validar horas
        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise serializers.ValidationError("La hora de inicio debe ser menor a la hora de fin.")

        # 2. Validar campos requeridos por tipo
        if tipo == 'recurrente' and not dia:
            raise serializers.ValidationError("Debe especificar el día de la semana para un horario recurrente.")
        if tipo == 'excepcion' and not fecha:
            raise serializers.ValidationError("Debe especificar la fecha para una excepción.")

        # 3. Validar traslape si es disponible
        qs = HorarioFlexible.objects.filter(
            cancha=cancha,
            tipo=tipo,
            diaSemana=dia if tipo == 'recurrente' else None,
            fecha=fecha if tipo == 'excepcion' else None,
        )
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if hora_inicio and hora_fin and disponible:
            traslape = qs.filter(
                horaInicio__lt=hora_fin,
                horaFin__gt=hora_inicio
            ).exists()
            if traslape:
                raise serializers.ValidationError("El horario se traslapa con uno ya existente.")

        # 4. Validar motivo si está bloqueado
        if not disponible and not motivo_bloqueo:
            raise serializers.ValidationError("Debe especificar un motivo si el horario está bloqueado.")

        return data