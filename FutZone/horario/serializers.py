from rest_framework import serializers
from .models import WeeklySchedule, DateException
from cancha.models import SoccerField


class WeeklyScheduleSerializer(serializers.ModelSerializer):
    cancha = serializers.CharField(source='cancha.name', read_only=True)
    cancha_id = serializers.PrimaryKeyRelatedField(
        queryset=SoccerField.objects.all(),
        source='cancha',
        write_only=True
    )
    dia_display = serializers.CharField(source='get_dia_display', read_only=True)

    class Meta:
        model = WeeklySchedule
        fields = [
            'id',
            'cancha',
            'cancha_id',
            'dia',
            'dia_display',
            'hora_apertura',
            'hora_cierre',
        ]
        read_only_fields = ['id', 'cancha', 'dia_display']

    def validate(self, attrs):
        cancha = attrs.get('cancha') or getattr(self.instance, 'cancha', None)
        dia = attrs.get('dia') or getattr(self.instance, 'dia', None)
        ap = attrs.get('hora_apertura')
        ci = attrs.get('hora_cierre')

        errors = {}
        if ap and ci and ap >= ci:
            errors['hora_apertura'] = ['La hora de apertura debe ser anterior a la de cierre.']

        qs = WeeklySchedule.objects.filter(cancha=cancha, dia=dia)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if ap and ci and qs.filter(hora_apertura__lt=ci, hora_cierre__gt=ap).exists():
            errors['hora_apertura'] = ['Este rango se traslapa con otro existente para ese día.']

        if errors:
            raise serializers.ValidationError(errors)
        return attrs

from rest_framework import serializers
from .models import DateException, SoccerField

class DateExceptionSerializer(serializers.ModelSerializer):
    cancha = serializers.CharField(source='cancha.name', read_only=True)
    cancha_id = serializers.PrimaryKeyRelatedField(
        queryset=SoccerField.objects.all(),
        source='cancha',
        write_only=True
    )
    cerrado_display = serializers.SerializerMethodField()

    class Meta:
        model = DateException
        fields = [
            'id',
            'cancha',
            'cancha_id',
            'fecha',
            'hora_apertura',
            'hora_cierre',
            'cerrado',
            'cerrado_display',
            'motivo',
        ]
        read_only_fields = ['id', 'cancha', 'cerrado_display']

    def get_cerrado_display(self, obj):
        return 'Sí' if obj.cerrado else 'No'

    def to_internal_value(self, data):
        # Si está cerrado, asignar horas por defecto si están vacías o None
        if data.get('cerrado'):
            if data.get('hora_apertura') in ['', None]:
                data['hora_apertura'] = "00:00"
            if data.get('hora_cierre') in ['', None]:
                data['hora_cierre'] = "23:59"
        return super().to_internal_value(data)

    def validate(self, attrs):
        cancha = attrs.get('cancha') or getattr(self.instance, 'cancha', None)
        fecha = attrs.get('fecha') or getattr(self.instance, 'fecha', None)
        ap = attrs.get('hora_apertura')
        ci = attrs.get('hora_cierre')
        cerrado = attrs.get('cerrado', getattr(self.instance, 'cerrado', True))
        motivo = attrs.get('motivo', getattr(self.instance, 'motivo', ''))

        errors = {}

        if cerrado:
            # Si está cerrado, no hace falta hora_apertura ni hora_cierre, pero en to_internal_value ya se ponen valores por defecto
            if not motivo:
                errors['motivo'] = ['Debe indicar un motivo si la cancha está cerrada ese día.']
        else:
            if not ap or not ci:
                errors['hora_apertura'] = ['Debe especificar hora de apertura si no está cerrado.']
                errors['hora_cierre'] = ['Debe especificar hora de cierre si no está cerrado.']
            elif ap >= ci:
                errors['hora_apertura'] = ['La hora de apertura debe ser anterior a la de cierre.']

        # Verificar traslapes con otras excepciones para la misma cancha y fecha
        qs = DateException.objects.filter(cancha=cancha, fecha=fecha)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if not cerrado and ap and ci and qs.filter(hora_apertura__lt=ci, hora_cierre__gt=ap).exists():
            errors['hora_apertura'] = ['El horario especial se traslapa con otra excepción para esa fecha.']

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
