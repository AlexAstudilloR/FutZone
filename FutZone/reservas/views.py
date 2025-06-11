from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from profiles.permissions import IsAdminOrOwnerWithLimitedEdit, IsAdminOrReadOnly
from profiles.models import ProfileModel
from profiles.authentication import SupabaseRemoteAuth

from django.utils.timezone import now
from datetime import datetime

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwnerWithLimitedEdit]
    authentication_classes = [SupabaseRemoteAuth]

    def get_queryset(self):
        user = self.request.user
        try:
            profile =ProfileModel.objects.get(id=self.request.user.id)  
        except ProfileModel.DoesNotExist:
            return Appointment.objects.none()

        if profile.is_admin:
            return Appointment.objects.all().order_by('id')
        return Appointment.objects.filter(user=profile)

    def perform_create(self, serializer):
        profile = ProfileModel.objects.get(id=self.request.user.id) 
        serializer.save(user=profile)

class ReservasPorFechaAPIView(APIView):
    """
    Devuelve todas las reservas creadas en una fecha específica (formato YYYY-MM-DD).
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

class DailyReservationSummaryAPIView(APIView):
    """
    Returns a daily summary of reservations: count, income, and occupied slots.
    Admin-only.
    """
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request):
        date_str = request.query_params.get('date')
        field_id = request.query_params.get('field_id')

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else now().date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        filters = {'date': date}
        if field_id:
            filters['field__id'] = field_id

        reservations = Appointment.objects.filter(**filters)

        total_reservations = reservations.count()
        total_income = sum(r.valor_pagar or 0 for r in reservations)

        if field_id:
            # Solo horarios de una cancha específica
            time_slots = [
                {"start": r.time_start.strftime("%H:%M"), "end": r.time_end.strftime("%H:%M")}
                for r in reservations
            ]
        else:
            # Agrupados por cancha
            time_slots = {}
            for r in reservations:
                field_name = r.field.name
                time_range = {
                    "start": r.time_start.strftime("%H:%M"),
                    "end": r.time_end.strftime("%H:%M")
                }
                time_slots.setdefault(field_name, []).append(time_range)

        response_data = {
            "date": date.isoformat(),
            "field_id": int(field_id) if field_id else None,
            "total_reservations": total_reservations,
            "total_income": f"{total_income:.2f}",
            "occupied_time_slots": time_slots,
        }

        return Response(response_data)