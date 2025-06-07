from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Appointment
from .serializers import AppointmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AppointmentViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class ReservasPorFechaAPIView(APIView):
    """
    Devuelve todas las reservas creadas en una fecha específica (formato YYYY-MM-DD).
    """
    def get(self, request):
        fecha = request.query_params.get('fecha')
        if not fecha:
            return Response(
                {"error": "Debe proporcionar el parámetro 'fecha' en formato YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reservas = Appointment.objects.filter(created_at__date=fecha)
        serializer = AppointmentSerializer(reservas, many=True)
        return Response(serializer.data)
