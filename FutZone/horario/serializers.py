from rest_framework import serializers
from .models import WeeklySchedule, DateException

class WeeklyScheduleSerializer(serializers.ModelSerializer):
    dia_display = serializers.CharField(source='get_dia_display', read_only=True)
    class Meta:
        model = WeeklySchedule
        fields = "__all__"
        read_only_fields = ["id", "dia_display"]

    def validate(self, attrs):
        cancha = attrs.get("cancha") or self.instance.cancha
        dia = attrs.get("dia") or self.instance.dia
        ap = attrs.get("hora_apertura")
        ci = attrs.get("hora_cierre")

        # 1. Apertura < cierre
        if ap and ci and ap >= ci:
            raise serializers.ValidationError("La hora de apertura debe ser anterior a la de cierre.")

        # 2. Traslape
        qs = WeeklySchedule.objects.filter(cancha=cancha, dia=dia)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if ap and ci and qs.filter(
            hora_apertura__lt=ci,
            hora_cierre__gt=ap
        ).exists():
            raise serializers.ValidationError("Este rango de horario se traslapa con otro existente para ese día.")

        return attrs


class DateExceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateException
        fields = "__all__"
        read_only_fields = ["id"]

    def validate(self, attrs):
        cancha = attrs.get("cancha") or self.instance.cancha
        fecha = attrs.get("fecha") or self.instance.fecha
        ap = attrs.get("hora_apertura")
        ci = attrs.get("hora_cierre")
        cerrado = attrs.get("cerrado", getattr(self.instance, "cerrado", True))
        motivo = attrs.get("motivo", getattr(self.instance, "motivo", ""))

        # 1. Si no está cerrado, apertura < cierre
        if not cerrado:
            if not ap or not ci:
                raise serializers.ValidationError("Debe especificar apertura y cierre si no está cerrado.")
            if ap >= ci:
                raise serializers.ValidationError("La hora de apertura debe ser anterior a la de cierre.")
        else:
            # 2. Si está cerrado, debe haber motivo
            if not motivo:
                raise serializers.ValidationError("Debe indicar un motivo si la cancha está cerrada ese día.")

        # 3. Traslape de excepciones en misma fecha
        qs = DateException.objects.filter(cancha=cancha, fecha=fecha)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        # Si tiene horas y no está cerrado, valida solapamiento
        if not cerrado and ap and ci and qs.filter(
            hora_apertura__lt=ci,
            hora_cierre__gt=ap
        ).exists():
            raise serializers.ValidationError("El horario especial se traslapa con otra excepción existente para esa fecha.")

        return attrs
