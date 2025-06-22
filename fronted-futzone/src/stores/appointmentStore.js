import { defineStore } from "pinia";
import * as appointmentService from "../services/appointmentService";
import * as XLSX from "xlsx";
import dayjs from "dayjs";
export const useAppointmentStore = defineStore("appointment", {
  state: () => ({
    appointments: [],
    summary: null,
    occupiedSlots: [],
    availableSlots: [],
    loading: false,
    error: null,
    totalCount: 0,
    next: null,
    previous: null,
    fieldSummaries: [],
  }),

  actions: {
    async fetchAppointments(page = 1, status = null) {
      this.loading = true;
      try {
        const res = await appointmentService.getAppointments(page, status);
        this.appointments = res.data.results;
        this.totalCount = res.data.count;
        this.next = res.data.next;
        this.previous = res.data.previous;
      } catch (err) {
        this.error = err;
      } finally {
        this.loading = false;
      }
    },

    async fetchDailySummary(date, fieldId = null) {
      this.loading = true;
      try {
        const res = fieldId
          ? await appointmentService.getAppointmentsByFieldAndDate(
              fieldId,
              date
            )
          : await appointmentService.getAppointmentsByDate(date);

        this.summary = res.data;
      } catch (err) {
        this.error = err;
      } finally {
        this.loading = false;
      }
    },

    async createAppointment(data) {
      try {
        const res = await appointmentService.createAppointment(data);
        return res.data;
      } catch (err) {
        throw err;
      }
    },

    async updateStatus(id, status) {
      try {
        await appointmentService.updateAppointmentStatus(id, status);
      } catch (err) {
        throw err;
      }
    },

    async fetchTimeSlots(date, fieldId, slotMinutes = 60) {
      this.loading = true;
      try {
        const res = await appointmentService.getTimeSlots(
          date,
          fieldId,
          slotMinutes
        );
        this.occupiedSlots = res.data.occupied_slots;
        this.availableSlots = res.data.available_slots;
      } catch (err) {
        this.error = err;
      } finally {
        this.loading = false;
      }
    },

    async fetchFieldSummaries(date) {
      this.loading = true;
      try {
        const res = await appointmentService.getFieldSummaryByDate(date);
        this.fieldSummaries = res.data.fields_summary;
      } catch (err) {
        this.error = err;
      } finally {
        this.loading = false;
      }
    },

    async exportReservationsExcel(param) {
      this.loading = true;
      try {
        const date =
          typeof param === "string"
            ? param
            : typeof param === "object" && param.date
            ? param.date
            : dayjs().format("YYYY-MM-DD");

        const [daily, fields] = await Promise.all([
          appointmentService.getAppointmentsByDate(date),
          appointmentService.getFieldSummaryByDate(date),
        ]);

        const resumenDiario = [
          {
            Fecha: daily.data.period,
            Total: daily.data.total_reservations,
            Aceptadas: daily.data.status_breakdown?.accepted || 0,
            Rechazadas: daily.data.status_breakdown?.rejected || 0,
            Pendientes: daily.data.status_breakdown?.pending || 0,
            Recaudado: daily.data.total_income,
            "Promedio Duración (min)": daily.data.average_duration_minutes,
            "Cancha más usada": daily.data.most_reserved_field || "N/A",
          },
        ];

        const resumenCanchas = (fields.data.fields_summary || []).map((f) => ({
          Cancha: f.field_name,
          Total: f.total_reservations,
          Aceptadas: f.status_breakdown?.accepted || 0,
          Rechazadas: f.status_breakdown?.rejected || 0,
          Pendientes: f.status_breakdown?.pending || 0,
          Recaudado: f.total_income,
          "Duración promedio (min)": f.average_duration_minutes,
        }));

        const wb = XLSX.utils.book_new();
        const sheetDiario = XLSX.utils.json_to_sheet(resumenDiario);
        const sheetCanchas = XLSX.utils.json_to_sheet(resumenCanchas);

        XLSX.utils.book_append_sheet(wb, sheetDiario, "Resumen Diario");
        XLSX.utils.book_append_sheet(wb, sheetCanchas, "Resumen por Cancha");

        XLSX.writeFile(wb, `Reporte_Reservas_${date}.xlsx`);
      } catch (err) {
        console.error("Error al exportar Excel:", err);
        throw err;
      } finally {
        this.loading = false;
      }
    },
  },
});
