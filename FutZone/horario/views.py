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

class HorariosExcepcionAPIView(APIView):
    """
    Devuelve los horarios excepcionales registrados para una fecha específica.
    """
    def get(self, request):
        fecha = request.query_params.get('fecha')
        if not fecha:
            return Response(
                {"error": "Debe proporcionar el parámetro 'fecha' en formato YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        excepciones = HorarioFlexible.objects.filter(tipo='excepcion', fecha=fecha)
        serializer = HorarioFlexibleSerializer(excepciones, many=True)
        return Response(serializer.data)