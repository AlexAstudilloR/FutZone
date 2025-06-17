from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from profiles.permissions import IsAdminOrReadOnly
from .models import WeeklySchedule, DateException
from .serializers import WeeklyScheduleSerializer, DateExceptionSerializer

class WeeklyScheduleViewSet(viewsets.ModelViewSet):

    queryset = WeeklySchedule.objects.all().order_by('cancha', 'dia')
    serializer_class = WeeklyScheduleSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=False, methods=['get'], url_path='dias-choices')
    def dias_choices(self, request):

        data = [
            {"value": val, "label": lbl}
            for val, lbl in WeeklySchedule.DIA_CHOICES
        ]
        return Response(data)


class DateExceptionViewSet(viewsets.ModelViewSet):
    """
    CRUD de excepciones de fecha.
    """
    queryset = DateException.objects.all().order_by('-fecha')
    serializer_class = DateExceptionSerializer
    permission_classes = [IsAdminOrReadOnly]


class DateExceptionByDateAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        fecha = request.query_params.get('fecha')
        if not fecha:
            return Response(
                {"error": "Debe proporcionar el parámetro 'fecha' en formato YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        excepciones = DateException.objects.filter(fecha=fecha)
        serializer = DateExceptionSerializer(excepciones, many=True)
        return Response(serializer.data)
