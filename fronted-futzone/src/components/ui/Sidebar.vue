<template>
  <aside
    v-if="authStore.isReady"
    :class="[
      'fixed top-0 left-0 h-full w-48 bg-blue-950 text-white p-4 flex flex-col justify-between z-40 transition-transform duration-300',
      isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0',
    ]"
  >
    <div>
      <div class="flex gap-2 px-2 py-1 mb-8 items-center">
        <img src="/logo.png" alt="" class="h-8 w-8" />
        <h1 class="text-xl font-semibold tracking-wide">FutZone</h1>
      </div>


      <nav class="space-y-2">
        <router-link
          v-if="authStore.profile?.is_admin"
          to="/admin"
          class="flex items-center gap-3 px-4 py-2 rounded-md transition duration-200 hover:bg-blue-900 hover:text-gray-200"
          :class="{
            'bg-blue-900 text-gray-200 font-semibold':
              $route.path.startsWith('/admin'),
          }"
        >
          <font-awesome-icon icon="gear" />
          <span>Administrar</span>
        </router-link>

        <router-link
          to="/canchas"
          class="flex items-center gap-3 px-4 py-2 rounded-md transition duration-200 hover:bg-blue-900 hover:text-gray-200"
          :class="{
            'bg-blue-900 text-gray-200 font-semibold':
              $route.path === '/canchas',
          }"
        >
          <font-awesome-icon icon="futbol" />
          <span>Canchas</span>
        </router-link>

        <router-link
          to="/profile"
          class="flex items-center gap-3 px-4 py-2 rounded-md transition duration-200 hover:bg-blue-900 hover:text-gray-200"
          :class="{
            'bg-blue-900 text-gray-200 font-semibold':
              $route.path === '/profile',
          }"
        >
          <font-awesome-icon icon="user" />
          <span>Mi perfil</span>
        </router-link>

        <router-link
          to="/reservar"
          class="flex items-center gap-3 px-4 py-2 rounded-md transition duration-200 hover:bg-blue-900 hover:text-gray-200"
          :class="{
            'bg-blue-900 text-gray-200 font-semibold':
              $route.path === '/reservar',
          }"
        >
          <font-awesome-icon icon="calendar-check" />
          <span>Reservar</span>
        </router-link>
      </nav>
    </div>

    <!-- Botón logout -->
    <button
      class="flex items-center gap-3 px-4 py-2 rounded-md transition duration-200 hover:bg-blue-900 hover:text-gray-200"
      @click="handleLogout"
    >
      <font-awesome-icon icon="right-from-bracket" />
      <span>Cerrar sesión</span>
    </button>
  </aside>
</template>

<script setup>
import { useAuthStore } from "../../stores/authStore";
import { useRouter, useRoute } from "vue-router";

const authStore = useAuthStore();
const { logout } = authStore;

const props = defineProps(["isOpen"]);
const router = useRouter();
const $route = useRoute();

const handleLogout = async () => {
  await logout();
  router.push("/login");
};
</script>
