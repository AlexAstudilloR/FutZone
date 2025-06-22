from .common import viewsets, IsAuthenticated, SupabaseRemoteAuth
from .common import Response, APIView,status

from profiles.models import ProfileModel
from profiles.permissions import IsAdminOrOwnerWithLimitedEdit, IsAdminOrReadOnly

from ..models import Appointment
from ..serializers import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet principal para listar, crear y modificar reservas.
    Los usuarios normales ven solo sus reservas. Los admins, todas.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwnerWithLimitedEdit]
    authentication_classes = [SupabaseRemoteAuth]

    def get_queryset(self):
        try:
            profile = ProfileModel.objects.get(id=self.request.user.id)  
        except ProfileModel.DoesNotExist:
            return Appointment.objects.none()

        queryset = Appointment.objects.all() if profile.is_admin else Appointment.objects.filter(user=profile)

        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        profile = ProfileModel.objects.get(id=self.request.user.id) 
        serializer.save(user=profile)


class ReservasPorFechaAPIView(APIView):
    """
    Devuelve todas las reservas creadas en una fecha específica.
    Solo accesible por administradores.
    """
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

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
