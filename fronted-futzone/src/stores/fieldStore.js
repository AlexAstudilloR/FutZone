import { defineStore } from "pinia";
import {
  getFields,
  createField,
  updateField,
  deleteField,
} from "../services/fieldService";

export const useFieldStore = defineStore("fields", {
  state: () => ({
    fields: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchFields({ available = null } = {}) {
      this.loading = true;
      this.error = null;
      try {
        const res = await getFields(available !== null ? { available } : {});
        this.fields = res.data.results || res.data;
      } catch (err) {
        this.error = err.response?.data || "Error al cargar canchas";
      } finally {
        this.loading = false;
      }
    },

    async createField(formData) {
      this.error = null;
      try {
        console.log("Enviando formData al service:", formData);

        // Usar la función createField del service importada
        const response = await createField(formData);

        this.fields.push(response.data);
        return { success: true };
      } catch (error) {
        console.error("Error en createField store:", error);
        this.error = error.response?.data || { general: "Error desconocido" };
        return {
          success: false,
          error: this.error,
        };
      }
    },

    async updateField(id, data) {
      this.error = null;
      try {
        const res = await updateField(id, data);
        const index = this.fields.findIndex((f) => f.id === id);
        if (index !== -1) this.fields[index] = res.data;
        return { success: true };
      } catch (err) {
        this.error = err.response?.data || "Error al actualizar cancha";
        return { success: false, error: this.error };
      }
    },

    async deleteField(id) {
      this.error = null;
      try {
        await deleteField(id);
        this.fields = this.fields.filter((f) => f.id !== id);
        return { success: true };
      } catch (err) {
        this.error = err.response?.data || "Error al eliminar cancha";
        return { success: false, error: this.error };
      }
    },
  },
});
