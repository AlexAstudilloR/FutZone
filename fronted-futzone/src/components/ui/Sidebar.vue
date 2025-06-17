<template>
  <aside
    :class="[
      'fixed top-0 left-0 h-full w-48 bg-[#19296D] text-white p-4 flex flex-col justify-between z-40 transition-transform duration-300',
      isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0',
    ]"
  >
    <div>
      <div class="flex items-center space-x-2">
        <img src="/logo.png" alt="Logo" class="h-10 w-auto" />
        <h1 class="text-lg font-bold">FutZone</h1>
      </div>

      <nav class="space-y-2 mt-6">
        <router-link
          v-if="authStore.profile?.is_admin"
          to="/admin"
          class="flex items-center gap-3 px-4 py-2 rounded-md transition-colors duration-200 ease-in-out hover:bg-[#15215c] hover:text-gray-200"
        >
          <font-awesome-icon icon="gear" class="transition-colors duration-200" />
          <span>Administrar</span>
        </router-link>

        <router-link
          to="/canchas"
          class="flex items-center gap-3 px-4 py-2 rounded-md transition-colors duration-200 ease-in-out hover:bg-[#15215c] hover:text-gray-200"
        >
          <font-awesome-icon icon="futbol" class="transition-colors duration-200" />
          <span>Canchas</span>
        </router-link>

        <router-link
          to="/perfil"
          class="flex items-center gap-3 px-4 py-2 rounded-md transition-colors duration-200 ease-in-out hover:bg-[#15215c] hover:text-gray-200"
        >
          <font-awesome-icon icon="user" class="transition-colors duration-200" />
          <span>Mi perfil</span>
        </router-link>

        <router-link
          to="/reservar"
          class="flex items-center gap-3 px-4 py-2 rounded-md transition-colors duration-200 ease-in-out hover:bg-[#15215c] hover:text-gray-200"
        >
          <font-awesome-icon icon="calendar-check" class="transition-colors duration-200" />
          <span>Reservar</span>
        </router-link>
      </nav>
    </div>

    <button
      class="flex items-center gap-3 px-4 py-2 rounded-md transition-colors duration-200 ease-in-out hover:bg-[#15215c] hover:text-gray-200"
      @click="handleLogout"
    >
      <font-awesome-icon icon="right-from-bracket" class="transition-colors duration-200" />
      <span>Cerrar sesión</span>
    </button>
  </aside>
</template>

<script setup>
import { useAuthStore } from "../../stores/authStore";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const { logout } = authStore;

const props = defineProps(["isOpen"]);
const router = useRouter();

const handleLogout = async () => {
  await logout();
  router.push("/login");
};
</script>
