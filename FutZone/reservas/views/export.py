from .common import (
    APIView, Response, IsAuthenticated, status,
    HttpResponse, Count, now, datetime,
    Workbook, get_column_letter, Font
)

from profiles.permissions import IsAdminOrReadOnly
from ..models import Appointment

class ExportReservationReportAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request):
        date_str = request.query_params.get("date")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else now().date()
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD."}, status=400)

        reservations = Appointment.objects.filter(date=date)
        accepted = reservations.filter(status="accepted")
        total_income = sum(r.valor_pagar or 0 for r in accepted)

        status_counts = reservations.values("status").annotate(count=Count("id"))
        status_summary = {entry["status"]: entry["count"] for entry in status_counts}

        durations = [
            (datetime.combine(r.date, r.time_end) - datetime.combine(r.date, r.time_start)).total_seconds() / 60
            for r in reservations
        ]
        average_duration = round(sum(durations) / len(durations), 2) if durations else 0

        field_counts = reservations.values("field__name").annotate(count=Count("id")).order_by("-count")
        most_reserved_field = field_counts[0]["field__name"] if field_counts else None

        wb = Workbook()


        ws1 = wb.active
        ws1.title = "Resumen Diario"
        resumen_data = [
            ["Fecha", "Total Reservas", "Ingresos", "Duración Promedio", "Cancha Más Reservada"],
            [date.isoformat(), reservations.count(), total_income, average_duration, most_reserved_field],
            [],
            ["Estado", "Cantidad"]
        ]
        for row in resumen_data:
            ws1.append(row)
        for status_key, count in status_summary.items():
            ws1.append([status_key, count])


        ws2 = wb.create_sheet(title="Por Cancha")
        ws2.append(["Cancha", "Reservas", "Ingresos", "Duración Promedio"])
        for field in field_counts:
            f_name = field["field__name"]
            field_reservations = reservations.filter(field__name=f_name)
            field_accepted = field_reservations.filter(status="accepted")
            income = sum(r.valor_pagar or 0 for r in field_accepted)
            durations = [
                (datetime.combine(r.date, r.time_end) - datetime.combine(r.date, r.time_start)).total_seconds() / 60
                for r in field_reservations
            ]
            avg = round(sum(durations) / len(durations), 2) if durations else 0
            ws2.append([f_name, field["count"], income, avg])


        ws3 = wb.create_sheet(title="Detalle del Día")
        ws3.append(["Cancha", "Hora Inicio", "Hora Fin", "Estado", "Valor a Pagar"])
        for r in reservations:
            ws3.append([
                r.field.name,
                r.time_start.strftime("%H:%M"),
                r.time_end.strftime("%H:%M"),
                r.status,
                r.valor_pagar or 0
            ])


        for sheet in wb.worksheets:
            for col in sheet.columns:
                max_length = max(len(str(cell.value)) if cell.value is not None else 0 for cell in col)
                col_letter = get_column_letter(col[0].column)
                sheet.column_dimensions[col_letter].width = max_length + 2
            for cell in sheet[1]:
                cell.font = Font(bold=True)

        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        filename = f"reporte_reservas_{date.isoformat()}.xlsx"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        wb.save(response)
        return response
