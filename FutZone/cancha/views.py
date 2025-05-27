from rest_framework import viewsets
from .models import SoccerField
from .serializer import FieldSerializer

class FieldViewSet(viewsets.ModelViewSet):
    queryset= SoccerField.objects.all()
    serializer_class= FieldSerializer