from rest_framework import serializers
from .models import SoccerField

#Serializador para el modelo de cancha 
class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoccerField
        fields= ['id', 'name','field_type','price','available']