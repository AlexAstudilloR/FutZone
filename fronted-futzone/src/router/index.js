import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/authStore";
import { storeToRefs } from "pinia";

// Vistas públicas y auth
const NotFound = () => import("../views/user/NotFound.vue");
const LandingPage = () => import("../views/user/Landing.vue");
const Login = () => import("../views/user/Login.vue");
const Register = () => import("../views/user/Register.vue");

// Vistas usuario autenticado
const ListSoccerField = () => import("../views/user/ListSoccerField.vue");
const MakeAppointment = () => import("../views/user/MakeAppointment.vue");
const Profile = () => import("../views/user/Profile.vue");

// Vistas admin (normales, sin children)
const AdminDashboard = () => import("../views/admin/AdminDashboard.vue");
const ManageAppointments = () => import("../views/admin/ManageAppointment.vue");
const ManageFields = () => import("../views/admin/ManageFields.vue");
const ManageSchedules = () => import("../views/admin/ManageSchedules.vue");
const ProfileAdmin = () => import("../views/admin/ProfileAdmin.vue");

const routes = [
  // Redirección raíz
  {
    path: "/",
    redirect: "/home",
  },

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

  // Rutas usuario
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

  // Rutas admin sin layout separado
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

  if (!isReady.value) {
    await authStore.init();
  }

  if (to.meta.requiresAuth && !token.value) {
    return next("/login");
  }

  if (to.meta.requiresAdmin && !profile.value?.is_admin) {
    return next("/profile");
  }

  next();
});

export default router;
