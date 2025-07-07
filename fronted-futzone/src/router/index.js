import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/authStore";
import { storeToRefs } from "pinia";

// Vistas públicas y auth
const NotFound         = () => import("../views/user/NotFound.vue");
const LandingPage      = () => import("../views/user/Landing.vue");
const Login            = () => import("../views/user/Login.vue");
const Register         = () => import("../views/user/Register.vue");
const RecoverPassword  = () => import("../views/user/PasswordRecovery.vue");
const ResetPassword    = () => import("../views/user/ResetPassword.vue");

// Vistas usuario autenticado
const ListSoccerField  = () => import("../views/user/ListSoccerField.vue");
const MakeAppointment  = () => import("../views/user/MakeAppointment.vue");
const Profile          = () => import("../views/user/Profile.vue");

// Vistas admin
const AdminDashboard   = () => import("../views/admin/AdminDashboard.vue");
const ManageAppointments = () => import("../views/admin/ManageAppointment.vue");
const ManageFields       = () => import("../views/admin/ManageFields.vue");
const ManageSchedules    = () => import("../views/admin/ManageSchedules.vue");
const ProfileAdmin       = () => import("../views/admin/ProfileAdmin.vue");

const routes = [
  // Redirección raíz
  { path: "/", redirect: "/home" },

  // Página pública principal
  {
    path: "/home",
    name: "Landing",
    component: LandingPage,
    meta: { layout: "none" },
  },

  // Rutas de auth
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: { layout: "auth" },
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
    meta: { layout: "auth" },
  },
  {
    path: "/recover-password",
    name: "RecoverPassword",
    component: RecoverPassword,
    meta: { layout: "auth" },
  },
  {
    path: "/reset-password",
    name: "ResetPassword",
    component: ResetPassword,
    meta: { layout: "auth" },
  },

  // Rutas usuario autenticado
  {
    path: "/canchas",
    name: "Canchas",
    component: ListSoccerField,
    meta: { layout: "default", requiresAuth: true },
  },
  {
    path: "/reservar",
    name: "Reservar",
    component: MakeAppointment,
    meta: { layout: "default", requiresAuth: true },
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
    meta: { layout: "default", requiresAuth: true },
  },

  // Rutas admin
  {
    path: "/admin",
    name: "AdminDashboard",
    component: AdminDashboard,
    meta: { layout: "default", requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin/schedules",
    name: "ManageSchedules",
    component: ManageSchedules,
    meta: { layout: "default", requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin/fields",
    name: "ManageFields",
    component: ManageFields,
    meta: { layout: "default", requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin/appointments",
    name: "ManageAppointments",
    component: ManageAppointments,
    meta: { layout: "default", requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/profile-admin",
    name: "AdminProfile",
    component: ProfileAdmin,
    meta: { layout: "default", requiresAuth: true, requiresAdmin: true },
  },

  // 404
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: NotFound,
    meta: { layout: "none" },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Protección global
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  const { token, profile, isReady } = storeToRefs(authStore);

  // Espera a inicializar el store (carga token & perfil si existe)
  if (!isReady.value) {
    await authStore.init();
  }

  // Si la ruta requiere autenticación y no hay token, redirige al login
  if (to.meta.requiresAuth && !token.value) {
    return next("/login");
  }

  // Si la ruta requiere rol admin y el usuario no es admin, lo mandas a su perfil
  if (to.meta.requiresAdmin && !profile.value?.is_admin) {
    return next("/profile");
  }

  // De lo contrario, continúa
  next();
});

export default router;
