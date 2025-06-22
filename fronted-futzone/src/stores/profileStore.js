import { defineStore } from "pinia";
import {
  getAllProfiles,
  createProfile,
  updateProfile,
  deleteProfile,
  registerUser,
} from "../services/authService";

export const useProfileStore = defineStore("profile", {
  state: () => ({
    profiles: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchProfiles({ includeInactive = false } = {}) {
      this.loading = true;
      try {
        const res = await getAllProfiles(includeInactive);
        this.profiles = res.data;
      } catch (err) {
        this.error = "Error al cargar los perfiles";
      } finally {
        this.loading = false;
      }
    },

    async addProfile(data) {
      this.error = null;
      try {
        const res = await createProfile(data);
        await this.fetchProfiles(); // refrescar lista
        return res.data;
      } catch (err) {
        this.error = err.response?.data || "Error al crear perfil.";
        throw this.error;
      }
    },

    async editProfile(id, data) {
      this.error = null;
      try {
        const res = await updateProfile(id, data);
        await this.fetchProfiles();
        return res.data;
      } catch (err) {
        this.error = err.response?.data || "Error al actualizar perfil.";
        throw this.error;
      }
    },

    async removeProfile(id) {
      this.error = null;
      try {
        await deleteProfile(id);
        await this.fetchProfiles(); 
      } catch (err) {
        this.error = "Error al eliminar perfil.";
        throw this.error;
      }
    },

    async createUserAndProfile(data) {
      this.error = null;
      try {
        const payload = { ...data };
        const isAdmin = payload.is_admin;
        delete payload.is_admin;

        const res = await registerUser(payload);
        const userId = res.data?.id;

        if (isAdmin && userId) {
          await updateProfile(userId, { is_admin: true });
        }

        await this.fetchProfiles();
        return res.data;
      } catch (err) {
        this.error = err.response?.data || "Error al registrar usuario.";
        throw this.error;
      }
    },
  },
});
