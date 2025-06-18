from rest_framework import serializers
from .models import SoccerField
import os
import re

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoccerField
        fields = ['id', 'name', 'field_type', 'price', 'available', 'image']

    def validate_name(self, value):
        normalized = value.strip()
        if len(normalized) < 6:
            raise serializers.ValidationError("El nombre debe tener al menos 6 caracteres.")
        if not re.match(r'^[a-zA-Z0-9\sáéíóúÁÉÍÓÚñÑ]+$', normalized):
            raise serializers.ValidationError("El nombre no puede contener símbolos ni caracteres especiales.")
        
        # Validar duplicado
        exists = SoccerField.objects.filter(name__iexact=normalized).exclude(id=self.instance.id if self.instance else None).exists()
        if exists:
            raise serializers.ValidationError("Ya existe una cancha con ese nombre.")
        
        return normalized

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo.")
        return value

    def validate_image(self, image):
        if image:
            ext = os.path.splitext(image.name)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png']
            if ext not in valid_extensions:
                raise serializers.ValidationError("El formato de imagen debe ser .jpg, .jpeg o .png.")
            if image.size > 2 * 1024 * 1024:
                raise serializers.ValidationError("La imagen no debe superar los 2MB.")
        return image
