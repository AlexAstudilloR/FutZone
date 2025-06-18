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
from django.db.models import Count
from django.utils.timezone import now
from datetime import datetime
from utils.slots import generate_slots, get_open_close

class AppointmentViewSet(viewsets.ModelViewSet):
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

        return queryset.order_by('id')
    def perform_create(self, serializer):
        profile = ProfileModel.objects.get(id=self.request.user.id) 
        serializer.save(user=profile)

class ReservasPorFechaAPIView(APIView):
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
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request):
        date_str   = request.query_params.get('date')    
        month_str  = request.query_params.get('month')    
        field_id   = request.query_params.get('field_id') 

        if date_str and month_str:
            return Response(
                {"error": "Use solo uno de los parámetros: 'date' o 'month'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        filters = {}
        try:
            if date_str:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                filters['date'] = date
            elif month_str:
                month_date = datetime.strptime(month_str, "%Y-%m")
                filters['date__year']  = month_date.year
                filters['date__month'] = month_date.month
            else:
                filters['date'] = now().date()
        except ValueError:
            return Response(
                {"error": "Formato de fecha inválido. Use YYYY-MM-DD o YYYY-MM."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if field_id:
            filters['field__id'] = field_id

        reservations = Appointment.objects.filter(**filters)

        # Recaudación solo de aceptadas
        accepted_reservations = reservations.filter(status='accepted')
        total_income = sum(r.valor_pagar or 0 for r in accepted_reservations)

        # Conteo por estado
        status_counts = reservations.values('status').annotate(count=Count('id'))
        status_summary = {entry['status']: entry['count'] for entry in status_counts}

        # Promedio de duración
        duraciones = [
            (datetime.combine(r.date, r.time_end) - datetime.combine(r.date, r.time_start)).total_seconds() / 60
            for r in reservations
        ]
        average_duration = round(sum(duraciones) / len(duraciones), 2) if duraciones else 0

        # Slots ocupados
        if field_id:
            time_slots = [
                {"start": r.time_start.strftime("%H:%M"), "end": r.time_end.strftime("%H:%M")}
                for r in reservations
            ]
        else:
            time_slots = {}
            for r in reservations:
                field_name = r.field.name
                time_range = {
                    "start": r.time_start.strftime("%H:%M"),
                    "end": r.time_end.strftime("%H:%M")
                }
                time_slots.setdefault(field_name, []).append(time_range)

        response_data = {
            "period": month_str or (date_str or now().date().isoformat()),
            "field_id": int(field_id) if field_id else None,
            "total_reservations": reservations.count(),
            "total_income": f"{total_income:.2f}",
            "occupied_time_slots": time_slots,
            "status_breakdown": status_summary,
            "average_duration_minutes": average_duration
        }

        return Response(response_data)
class ReservationStatusCountAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request):
        qs = Appointment.objects.values('status').annotate(count=Count('id'))
        counts_by_state = { entry['status']: entry['count'] for entry in qs }

        return Response(counts_by_state, status=status.HTTP_200_OK)
    
class TimeSlotAvailabilityAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request):
        date_str  = request.query_params.get('date')
        field_id  = request.query_params.get('field_id')
        slot_mins = int(request.query_params.get('slot_minutes', 60))

        try:
            fecha = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            return Response({"error": "date YYYY-MM-DD obligatorio"}, 400)

        apertura, cierre = get_open_close(field_id, fecha)
        if not apertura:
            return Response({"occupied_slots": [], "available_slots": [], "average_duration_minutes": 0})

        reservas = Appointment.objects.filter(date=fecha, field_id=field_id)

        occupied = [
            {"start": r.time_start.strftime("%H:%M"), "end": r.time_end.strftime("%H:%M")}
            for r in reservas
        ]

        all_slots = generate_slots(apertura, cierre, slot_mins)

        available = [
            s for s in all_slots
            if not any(s['start'] < o['end'] and o['start'] < s['end'] for o in occupied)
        ]

        duraciones = [
            (datetime.combine(fecha, r.time_end) - datetime.combine(fecha, r.time_start)).total_seconds() / 60
            for r in reservas
        ]
        promedio_minutos = round(sum(duraciones) / len(duraciones), 2) if duraciones else 0

        return Response({
            "occupied_slots": occupied,
            "available_slots": available,
            "average_duration_minutes": promedio_minutos
        })