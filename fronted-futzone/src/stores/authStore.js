import { defineStore } from "pinia";
import { supabase } from "../lib/supabase";
import { registerUser, getMyProfile } from "../services/authService";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    token: null,
    profile: null,
    error: null,
    isReady: false, 
  }),

  actions: {
    async init() {
      this.isReady = false; 
      const token = localStorage.getItem("access_token");
      if (!token) {
        this.isReady = true;
        return;
      }

      this.token = token;

      try {
        const { data, error } = await supabase.auth.getUser();
        if (error || !data.user) {
          console.warn("No se pudo recuperar usuario:", error);
          await this.logout();
          return;
        }

        this.user = data.user;

        const profileRes = await getMyProfile();
        this.profile = profileRes.data;
      } catch (err) {
        console.error("Error al inicializar sesión:", err);
        await this.logout();
      } finally {
        this.isReady = true; 
      }
    },

    async login(email, password) {
      this.error = null;
      this.isReady = false;

      try {
        const { data, error } = await supabase.auth.signInWithPassword({
          email,
          password,
        });

        if (error) {
          const msg = error.message;
          if (msg === "Invalid login credentials") {
            this.error = "Correo o contraseña incorrectos";
          } else {
            this.error = "Error al iniciar sesión";
          }
          this.isReady = true;
          return false;
        }

        this.user = data.user;
        this.token = data.session?.access_token;
        localStorage.setItem("access_token", this.token);

        const profileRes = await getMyProfile();
        this.profile = profileRes.data;

        return true;
      } catch (err) {
        this.error = "Error inesperado al intentar iniciar sesión";
        return false;
      } finally {
        this.isReady = true;
      }
    },

    async register(data) {
      this.error = null;
      try {
        const res = await registerUser(data);

        if (res.data?.error) {
          this.error = res.data.error;
          return { success: false, error: this.error };
        }

        return { success: true, data: res.data };
      } catch (err) {
        this.error = err.response?.data?.error || "Error al registrar usuario";
        return { success: false, error: this.error };
      }
    },

    async logout() {
      this.isReady = false;
      this.user = null;
      this.token = null;
      this.profile = null;
      this.error = null;
      localStorage.removeItem("access_token");
      await supabase.auth.signOut();
      this.isReady = true;
    },
  },
});
