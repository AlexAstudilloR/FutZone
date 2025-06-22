import { defineStore } from "pinia";
import * as appointmentService from "../services/appointmentService";

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
          ? await appointmentService.getAppointmentsByFieldAndDate(fieldId, date)
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
        const res = await appointmentService.getTimeSlots(date, fieldId, slotMinutes);
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
    }
  },
});
