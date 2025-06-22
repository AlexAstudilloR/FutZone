<template>
  <div class="p-6 space-y-8">
    <!-- Perfil del usuario -->
    <section class="bg-white shadow rounded-lg p-6 flex items-center gap-6">
      <div class="w-24 h-24 rounded-full overflow-hidden">
        <img
          src="/profile.jpeg"
          alt="Foto de perfil"
          class="w-full h-full object-cover rounded-full"
        />
      </div>
      <div class="flex flex-col">
        <h2 class="text-xl font-bold">{{ profile.full_name }}</h2>
        <p class="text-gray-600"><b>+593</b> {{ profile.cell_phone }}</p>
      </div>
    </section>

    <!-- Historial de reservas -->
    <section>
      <div class="flex gap-2 items-center mb-4">
        <h3 class="text-lg font-semibold">Historial de Reservas</h3>
        <font-awesome-icon icon="clock-rotate-left" />
      </div>

      <!-- Filtro de estado -->
      <div class="flex justify-end mb-4 w-full max-w-xs ml-auto">
        <BaseSelect
          v-model="selectedStatus"
          :options="statusOptions"
          placeholder="Filtrar por estado"
          size="sm"
        />
      </div>

      <!-- Lista de reservas con transición -->
      <transition name="fade" mode="out-in">
        <div
          :key="
            appointmentStore.loading
              ? 'loading'
              : appointmentStore.appointments.length === 0
              ? 'no-data'
              : 'data'
          "
        >
          <div v-if="appointmentStore.loading" class="space-y-4">
            <SkeletonCard
              v-for="n in 3"
              :key="n"
              :lines="4"
              avatar
              extra-class="h-[120px]"
            />
          </div>

          <NoData
            v-else-if="appointmentStore.appointments.length === 0"
            message="No tienes reservas aún."
          />

          <div v-else class="space-y-4">
            <AppointmentCard
              v-for="reserva in appointmentStore.appointments"
              :key="reserva.id"
              :appointment="reserva"
              :is-admin="authStore.profile?.is_admin"
            />
          </div>
        </div>
      </transition>

      <!-- Paginación -->
      <Pagination
        :current-page="currentPage"
        :total-items="appointmentStore.totalCount"
        @update:page="handlePageChange"
      />
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import AppointmentCard from "../../components/ui/AppointmentCard.vue";
import SkeletonCard from "../../components/ui/SkeletonCard.vue";
import Pagination from "../../components/ui/Pagination.vue";
import BaseSelect from "../../components/ui/BaseSelect.vue";
import NoData from "../../components/ui/NoData.vue";
import * as authService from "../../services/authService";
import { useAppointmentStore } from "../../stores/appointmentStore";
import { useAuthStore } from "../../stores/authStore";
const authStore = useAuthStore();
const profile = ref({});
const appointmentStore = useAppointmentStore();
const selectedStatus = ref("");
const currentPage = ref(1);

const statusOptions = [
  { value: "", label: "Todos" },
  { value: "pending", label: "Pendiente" },
  { value: "accepted", label: "Aceptada" },
  { value: "rejected", label: "Rechazada" },
];

const fetchProfile = async () => {
  const { data } = await authService.getMyProfile();
  profile.value = data;
};

const fetchAppointments = () => {
  appointmentStore.fetchAppointments(
    currentPage.value,
    selectedStatus.value || null
  );
};

const handlePageChange = (page) => {
  currentPage.value = page;
  fetchAppointments();
};

watch(selectedStatus, () => {
  currentPage.value = 1;
  fetchAppointments();
});

onMounted(async () => {
  await fetchProfile();
  fetchAppointments();
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.11s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
