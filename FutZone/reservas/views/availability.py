from .common import (
    APIView, Response, IsAuthenticated, datetime,
    generate_slots, get_open_close
)

from profiles.permissions import IsAdminOrReadOnly
from ..models import Appointment
class TimeSlotAvailabilityAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request):
        date_str  = request.query_params.get('date')
        field_id  = request.query_params.get('field_id')
        slot_mins = int(request.query_params.get('slot_minutes', 60))

        try:
            fecha = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            return Response({"error": "date YYYY-MM-DD obligatorio"}, status=400)

        apertura, cierre = get_open_close(field_id, fecha)
        if not apertura:
            return Response({
                "occupied_slots": [],
                "available_slots": [],
                "average_duration_minutes": 0
            })

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
