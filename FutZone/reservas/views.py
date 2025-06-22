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

        return queryset.order_by('-created_at')
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
        date_str = request.query_params.get('date')
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else now().date()
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD."}, status=400)

        reservations = Appointment.objects.filter(date=date)
        accepted = reservations.filter(status='accepted')
        total_income = sum(r.valor_pagar or 0 for r in accepted)

        status_counts = reservations.values('status').annotate(count=Count('id'))
        status_summary = {entry['status']: entry['count'] for entry in status_counts}

        duraciones = [
            (datetime.combine(r.date, r.time_end) - datetime.combine(r.date, r.time_start)).total_seconds() / 60
            for r in reservations
        ]
        average_duration = round(sum(duraciones) / len(duraciones), 2) if duraciones else 0

        field_counts = reservations.values('field__name').annotate(count=Count('id')).order_by('-count')
        most_reserved_field = field_counts[0]['field__name'] if field_counts else None

        return Response({
            "period": date.isoformat(),
            "total_reservations": reservations.count(),
            "total_income": f"{total_income:.2f}",
            "status_breakdown": status_summary,
            "average_duration_minutes": average_duration,
            "most_reserved_field": most_reserved_field
        })
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
        
class FieldReservationSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request):
        date_str = request.query_params.get('date')
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else now().date()
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD."}, status=400)

        reservations = Appointment.objects.filter(date=date)
        fields = reservations.values_list('field__id', 'field__name').distinct()
        summaries = []

        for f_id, f_name in fields:
            field_reservations = reservations.filter(field__id=f_id)
            accepted = field_reservations.filter(status='accepted')
            total_income = sum(r.valor_pagar or 0 for r in accepted)

            status_counts = field_reservations.values('status').annotate(count=Count('id'))
            status_summary = {entry['status']: entry['count'] for entry in status_counts}

            duraciones = [
                (datetime.combine(r.date, r.time_end) - datetime.combine(r.date, r.time_start)).total_seconds() / 60
                for r in field_reservations
            ]
            average_duration = round(sum(duraciones) / len(duraciones), 2) if duraciones else 0

            summaries.append({
                "field_id": f_id,
                "field_name": f_name,
                "total_reservations": field_reservations.count(),
                "total_income": f"{total_income:.2f}",
                "status_breakdown": status_summary,
                "average_duration_minutes": average_duration
            })

        return Response({
            "date": date.isoformat(),
            "fields_summary": summaries
        })