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

    async fetchSummary({ date = null, start_date = null, end_date = null }) {
      this.loading = true;
      try {
        const res = await appointmentService.getAppointmentsSummary({
          ...(date && { date }),
          ...(start_date && end_date ? { start_date, end_date } : {}),
        });
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

    async fetchFieldSummaries(params = {}) {
      this.loading = true;
      try {
        const res = await appointmentService.getFieldSummary(params);
        this.fieldSummaries = res.data.fields_summary;
      } catch (err) {
        this.error = err;
      } finally {
        this.loading = false;
      }
    },

    async exportReservationsExcel(params = {}) {
      this.loading = true;
      try {
        const response = await appointmentService.exportReservationReport(
          params
        );

        const blob = new Blob([response.data], {
          type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        });

        const period =
          params.date ||
          (params.start_date && params.end_date
            ? `${params.start_date}_a_${params.end_date}`
            : dayjs().format("YYYY-MM-DD"));

        const filename = `Reporte_Reservas_${period}.xlsx`;
        const link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);
        link.download = filename;
        link.click();
      } catch (err) {
        console.error("Error al exportar Excel:", err);
        throw err;
      } finally {
        this.loading = false;
      }
    },
  },
});
