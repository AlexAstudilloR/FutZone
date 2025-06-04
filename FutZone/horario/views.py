from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import HorarioFlexible
from .serializers import HorarioFlexibleSerializer

class HorarioFlexibleViewSet(viewsets.ModelViewSet):
    queryset = HorarioFlexible.objects.all()
    serializer_class = HorarioFlexibleSerializer
    permission_classes = [AllowAny]  # Reemplazar después por permisos para admin

