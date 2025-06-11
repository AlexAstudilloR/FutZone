import { defineStore } from "pinia";
import { supabase } from "../lib/supabase";
import { registerUser, getMyProfile } from "../services/authService";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    token: null,
    profile: null,
    error: null,
  }),
  actions: {
    async init() {
      const token = localStorage.getItem("access_token");
      if (!token) return;

      this.token = token;

      try {
        const { data, error } = await supabase.auth.getUser();
        if (error || !data.user) {
          console.warn("⚠️ No se pudo recuperar usuario:", error);
          await this.logout();
          return;
        }

        this.user = data.user;

        const profileRes = await getMyProfile();
        this.profile = profileRes.data;
      } catch (err) {
        console.error("❌ Error al inicializar sesión:", err);
        await this.logout();
      }
    },

    async login(email, password) {
      this.error = null;
      try {
        const { data, error } = await supabase.auth.signInWithPassword({
          email,
          password,
        });

        if (error) {
          this.error = error.message;
          return false;
        }

        this.user = data.user;
        this.token = data.session?.access_token;
        localStorage.setItem("access_token", this.token);

        const profileRes = await getMyProfile();
        this.profile = profileRes.data;

        return true;
      } catch (err) {
        console.error("💥 Error al iniciar sesión:", err);
        this.error = "Error inesperado al intentar iniciar sesión";
        return false;
      }
    },

    async register(payload) {
      this.error = null;
      try {
        const res = await registerUser(payload);
        return { success: true, data: res.data };
      } catch (err) {
        this.error = err.response?.data || "Error en el registro";
        return { success: false, error: this.error };
      }
    },

    async logout() {
      this.user = null;
      this.token = null;
      this.profile = null;
      this.error = null;
      localStorage.removeItem("access_token");
      await supabase.auth.signOut();
    },
  },
});
