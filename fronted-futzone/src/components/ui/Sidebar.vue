<template>
  <aside
    :class="[
      'fixed top-0 left-0 h-full w-48 bg-[#19296D] text-white p-4 flex flex-col justify-between z-40 transition-transform duration-300',
      isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0',
    ]"
  >

    <div>
      <!-- Logo -->
      <div class="flex items-center space-x-2">
        <img src="/logo.png" alt="Logo" class="h-10 w-auto" />
        <h1 class="text-lg font-bold">FutZone</h1>
      </div>


      <nav class="space-y-2 mt-6">
        <router-link
          v-if="authStore.profile?.is_admin"
          to="/admin"
          class="flex items-center gap-3 px-4 py-2 rounded-md hover:bg-[#15215c] transition"
        >
          <font-awesome-icon icon="gear" />
          <span>Administrar</span>
        </router-link>
        <router-link
          to="/canchas"
          class="flex items-center gap-3 px-4 py-2 rounded-md hover:bg-[#15215c] transition"
        >
          <font-awesome-icon icon="futbol" />
          <span>Canchas</span>
        </router-link>
        <router-link
          to="/perfil"
          class="flex items-center gap-3 px-4 py-2 rounded-md hover:bg-[#15215c] transition"
        >
          <font-awesome-icon icon="user" />
          <span>Mi perfil</span>
        </router-link>
        <router-link
          to="/mis-reservas"
          class="flex items-center gap-3 px-4 py-2 rounded-md hover:bg-[#15215c] transition"
        >
          <font-awesome-icon icon="calendar-check" />
          <span>Mis reservas</span>
        </router-link>
        <router-link
          to="/reservas"
          class="flex items-center gap-3 px-4 py-2 rounded-md hover:bg-[#15215c] transition"
        >
          <font-awesome-icon icon="calendar-check" />
          <span>Reservar</span>
        </router-link>


      </nav>
    </div>


    <button
      class="flex items-center gap-3 px-4 py-2 rounded-md hover:bg-[#15215c] transition"
      @click="handleLogout"
    >
      <font-awesome-icon icon="right-from-bracket" />
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
