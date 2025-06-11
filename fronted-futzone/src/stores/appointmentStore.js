// stores/appointmentStore.js
import { defineStore } from "pinia";
import * as appointmentService from "../services/appointmentService";
export const useAppointmentStore = defineStore("appointment", {
  state: () => ({
    appointments: [],
    summary: null,
    loading: false,
    error: null,
  }),

  actions: {
    async fetchAppointments(page = 1) {
      this.loading = true;
      try {
        const res = await appointmentService.getAppointments(page);
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
  },
});
