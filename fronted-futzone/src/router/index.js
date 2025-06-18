import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/authStore";
import { storeToRefs } from "pinia";
import NotFound from "../views/user/NotFound.vue";

const ListSoccerField = () => import("../views/user/ListSoccerField.vue");
const LandingPage = () => import("../views/user/Landing.vue");
const AdminDashboard = () => import("../views/admin/AdminDashboard.vue");
const Login = () => import("../views/user/Login.vue");
const Register = () => import("../views/user/Register.vue");
const ManageAppointments = () => import("../views/admin/ManageAppointment.vue");
const ManageFields = () => import("../views/admin/ManageFields.vue");
const ManageSchedules = () => import("../views/admin/ManageSchedules.vue");
const MakeAppointment = () => import("../views/user/MakeAppointment.vue");
const Profile = () => import("../views/user/Profile.vue");
const routes = [
  {
    path: "/",
    redirect: "/home",
  },
  {
    path: "/home",
    name: "Landing",
    component: LandingPage,
    meta: { layout: "none" },
  },
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
    path: "/admin",
    name: "AdminDashboard",
    component: AdminDashboard,
    meta: { layout: "default", requiresAuth: true },
  },
  {
    path: "/admin/schedules",
    name: "ManageSchedules",
    component: ManageSchedules,
    meta: { layout: "default", requiresAuth: true },
  },
  {
    path: "/admin/fields",
    name: "ManageFields",
    component: ManageFields,
    meta: { layout: "default", requiresAuth: true },
  },
  {
    path: "/admin/appointments",
    name: "ManageAppointments",
    component: ManageAppointments,
    meta: { layout: "default", requiresAuth: true },
  },
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
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const { token } = storeToRefs(authStore);

  if (to.meta.requiresAuth && !token.value) {
    return next("/login");
  }

  next();
});
export default router;
