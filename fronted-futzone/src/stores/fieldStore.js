import { defineStore } from 'pinia'
import {
  getFields,
  createField,
  updateField,
  deleteField
} from '../services/fieldService'

export const useFieldStore = defineStore('fields', {
  state: () => ({
    fields: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchFields({ available = null } = {}) {
      this.loading = true
      this.error = null
      try {
        const res = await getFields(available !== null ? { available } : {})
        this.fields = res.data.results || res.data
      } catch (err) {
        this.error = err.response?.data || 'Error al cargar canchas'
      } finally {
        this.loading = false
      }
    },

    async createField(data) {
      this.error = null
      try {
        const res = await createField(data)
        this.fields.push(res.data)
        return { success: true }
      } catch (err) {
        this.error = err.response?.data || 'Error al crear cancha'
        return { success: false, error: this.error }
      }
    },

    async updateField(id, data) {
      this.error = null
      try {
        const res = await updateField(id, data)
        const index = this.fields.findIndex(f => f.id === id)
        if (index !== -1) this.fields[index] = res.data
        return { success: true }
      } catch (err) {
        this.error = err.response?.data || 'Error al actualizar cancha'
        return { success: false, error: this.error }
      }
    },

    async deleteField(id) {
      this.error = null
      try {
        await deleteField(id)
        this.fields = this.fields.filter(f => f.id !== id)
        return { success: true }
      } catch (err) {
        this.error = err.response?.data || 'Error al eliminar cancha'
        return { success: false, error: this.error }
      }
    },
  },
})
