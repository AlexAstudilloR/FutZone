
import { defineStore } from 'pinia'
import {
  getWeeklySchedules,
  createWeeklySchedule,
  updateWeeklySchedule,
  deleteWeeklySchedule,
  getDiasChoices,
  getDateExceptions,
  getExceptionsByDate,
  createDateException,
  updateDateException,
  deleteDateException,
} from '../services/scheduleService'

export const useScheduleStore = defineStore('schedules', {
  state: () => ({
    weekly: [],
    diasChoices: [],
    exceptions: [],
    loading: false,
    error: null,
    formErrors: {},    
  }),

  actions: {


    async fetchWeekly(params = {}) {
      this.loading = true
      this.error = null
      try {
        const res = await getWeeklySchedules(params)
        this.weekly = res.data.results || res.data
      } catch (err) {
        this.error = err.response?.data || 'Error al cargar horarios semanales'
      } finally {
        this.loading = false
      }
    },

    async createWeekly(data) {
      this.error = null
      this.formErrors = {}
      try {
        const res = await createWeeklySchedule(data)
        this.weekly.push(res.data)
        return { success: true }
      } catch (err) {
        if (err.response?.data && typeof err.response.data === 'object') {
          this.formErrors = err.response.data
        } else {
          this.error = err.response?.data || 'Error al crear horario semanal'
        }
        return { success: false, errors: this.formErrors || this.error }
      }
    },

    async updateWeekly(id, data) {
      this.error = null
      this.formErrors = {}
      try {
        const res = await updateWeeklySchedule(id, data)
        const idx = this.weekly.findIndex(w => w.id === id)
        if (idx !== -1) this.weekly[idx] = res.data
        return { success: true }
      } catch (err) {
        if (err.response?.data && typeof err.response.data === 'object') {
          this.formErrors = err.response.data
        } else {
          this.error = err.response?.data || 'Error al actualizar horario semanal'
        }
        return { success: false, errors: this.formErrors || this.error }
      }
    },

    async deleteWeekly(id) {
      this.error = null
      try {
        await deleteWeeklySchedule(id)
        this.weekly = this.weekly.filter(w => w.id !== id)
        return { success: true }
      } catch (err) {
        this.error = err.response?.data || 'Error al eliminar horario semanal'
        return { success: false, error: this.error }
      }
    },

    // ------------------------
    // Día Choices
    // ------------------------

    async fetchDiasChoices() {
      this.error = null
      try {
        const res = await getDiasChoices()
        this.diasChoices = res.data
        return { success: true }
      } catch (err) {
        this.error = err.response?.data || 'Error al cargar choices de días'
        return { success: false, error: this.error }
      }
    },



    async fetchExceptions(params = {}) {
      this.loading = true
      this.error = null
      try {
        const res = await getDateExceptions(params)
        this.exceptions = res.data.results || res.data
      } catch (err) {
        this.error = err.response?.data || 'Error al cargar excepciones'
      } finally {
        this.loading = false
      }
    },

    async fetchExceptionsByDate(fecha) {
      this.loading = true
      this.error = null
      try {
        const res = await getExceptionsByDate(fecha)
        this.exceptions = res.data
      } catch (err) {
        this.error = err.response?.data || 'Error al cargar excepciones por fecha'
      } finally {
        this.loading = false
      }
    },

    async createException(data) {
      this.error = null
      this.formErrors = {}
      try {
        const res = await createDateException(data)
        this.exceptions.push(res.data)
        return { success: true }
      } catch (err) {
        if (err.response?.data && typeof err.response.data === 'object') {
          this.formErrors = err.response.data
        } else {
          this.error = err.response?.data || 'Error al crear excepción'
        }
        return { success: false, errors: this.formErrors || this.error }
      }
    },

    async updateException(id, data) {
      this.error = null
      this.formErrors = {}
      try {
        const res = await updateDateException(id, data)
        const idx = this.exceptions.findIndex(e => e.id === id)
        if (idx !== -1) this.exceptions[idx] = res.data
        return { success: true }
      } catch (err) {
        if (err.response?.data && typeof err.response.data === 'object') {
          this.formErrors = err.response.data
        } else {
          this.error = err.response?.data || 'Error al actualizar excepción'
        }
        return { success: false, errors: this.formErrors || this.error }
      }
    },

    async deleteException(id) {
      this.error = null
      try {
        await deleteDateException(id)
        this.exceptions = this.exceptions.filter(e => e.id !== id)
        return { success: true }
      } catch (err) {
        this.error = err.response?.data || 'Error al eliminar excepción'
        return { success: false, error: this.error }
      }
    },
  },
})
