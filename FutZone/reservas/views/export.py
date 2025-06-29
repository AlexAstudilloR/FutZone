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
        start_str = request.query_params.get("start_date")
        end_str = request.query_params.get("end_date")
        date_str = request.query_params.get("date")

        try:
            if start_str and end_str:
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
                reservations = Appointment.objects.filter(date__range=(start_date, end_date))
                period_label = f"{start_date.isoformat()}_a_{end_date.isoformat()}"
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

        # Hoja 1: Resumen
        ws1 = wb.active
        ws1.title = "Resumen"
        ws1.append(["Periodo", "Total Reservas", "Ingresos", "Duración Promedio (min)", "Cancha Más Reservada"])
        ws1.append([period_label, reservations.count(), total_income, average_duration, most_reserved_field])
        ws1.append([])
        ws1.append(["Estado", "Cantidad"])
        for status_key, count in status_summary.items():
            ws1.append([status_key, count])

        # Hoja 2: Por cancha
        ws2 = wb.create_sheet(title="Por Cancha")
        ws2.append(["Cancha", "Reservas", "Ingresos $", "Duración Promedio (min)"])
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

        # Hoja 3: Detalle
        ws3 = wb.create_sheet(title="Detalle")
        ws3.append(["Fecha", "Cancha", "Hora Inicio", "Hora Fin", "Estado", "Valor a Pagar"])
        for r in reservations:
            ws3.append([
                r.date.isoformat(),
                r.field.name,
                r.time_start.strftime("%H:%M"),
                r.time_end.strftime("%H:%M"),
                r.status,
                r.valor_pagar or 0
            ])

        # Estilos generales
        for sheet in wb.worksheets:
            for col in sheet.columns:
                max_length = max(len(str(cell.value)) if cell.value is not None else 0 for cell in col)
                col_letter = get_column_letter(col[0].column)
                sheet.column_dimensions[col_letter].width = max_length + 2
            for cell in sheet[1]:
                cell.font = Font(bold=True)

        # Exportación final
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        filename = f"reporte_reservas_{period_label}.xlsx"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        wb.save(response)
        return response
