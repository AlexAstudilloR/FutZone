from .common import (
    APIView, Response, IsAuthenticated, status,
    Count, datetime, now
)
from profiles.permissions import IsAdminOrReadOnly
from ..models import Appointment

class DailyReservationSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request):
        start_str = request.query_params.get('start_date')
        end_str = request.query_params.get('end_date')
        date_str = request.query_params.get('date')

        try:
            if start_str and end_str:
                start = datetime.strptime(start_str, "%Y-%m-%d").date()
                end = datetime.strptime(end_str, "%Y-%m-%d").date()
                reservations = Appointment.objects.filter(date__range=(start, end))
                period_label = f"{start.isoformat()} to {end.isoformat()}"
            elif date_str:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                reservations = Appointment.objects.filter(date=date)
                period_label = date.isoformat()
            else:
                today = now().date()
                reservations = Appointment.objects.filter(date=today)
                period_label = today.isoformat()
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD."}, status=400)

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
            "period": period_label,
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
        counts_by_state = {entry['status']: entry['count'] for entry in qs}

        return Response(counts_by_state, status=status.HTTP_200_OK)


class FieldReservationSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request):
        start_str = request.query_params.get('start_date')
        end_str = request.query_params.get('end_date')
        date_str = request.query_params.get('date')

        try:
            if start_str and end_str:
                start = datetime.strptime(start_str, "%Y-%m-%d").date()
                end = datetime.strptime(end_str, "%Y-%m-%d").date()
                reservations = Appointment.objects.filter(date__range=(start, end))
                period_label = f"{start.isoformat()} to {end.isoformat()}"
            elif date_str:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                reservations = Appointment.objects.filter(date=date)
                period_label = date.isoformat()
            else:
                today = now().date()
                reservations = Appointment.objects.filter(date=today)
                period_label = today.isoformat()
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD."}, status=400)

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
            "period": period_label,
            "fields_summary": summaries
        })