from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import  HorarioDisponible
from .serializers import  HorarioDisponibleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HorarioDisponibleViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = HorarioDisponible.objects.all()
    serializer_class = HorarioDisponibleSerializer


class HorariosFiltradosAPIView(APIView):
    def get(self, request):
        dia = request.query_params.get('diaSemana')
        cancha = request.query_params.get('cancha')

        if not dia or not cancha:
            return Response({'error': 'Parámetros "diaSemana" y "cancha" son requeridos.'},
                            status=status.HTTP_400_BAD_REQUEST)

        horarios = HorarioDisponible.objects.filter(
            diaSemana=dia,
            cancha=cancha,
            disponible=True
        )

        serializer = HorarioDisponibleSerializer(horarios, many=True)
        return Response(serializer.data)