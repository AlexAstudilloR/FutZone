<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Gestionar Reservas</h1>
      <LinkButton
        to="/admin"
        label="Volver a panel"
        :icon="['fas', 'arrow-left']"
        size="md"
        variant="none"
        color="inherit"
        extraClass="border border-[#19296D] text-[#19296D] hover:bg-[#19296D] hover:text-white transition-colors duration-200"
      />
    </div>

    <!-- Orden -->
    <div class="flex items-center gap-2 mb-6">
      <label>ordenar por fecha</label>
      <select
        v-model="sortOrder"
        @change="sortAppointments"
        class="border px-2 py-1 rounded"
      >
        <option value="asc">ascendente</option>
        <option value="desc">descendente</option>
      </select>
    </div>

    <div v-for="appointment in sortedAppointments" :key="appointment.id">
      <AppointmentCard
        :appointment="appointment"
        @accept="updateStatus(appointment.id, 'accepted')"
        @reject="updateStatus(appointment.id, 'rejected')"
      />
    </div>

    <Pagination
      v-if="!store.loading && store.totalCount > 0"
      :currentPage="currentPage"
      :totalItems="store.totalCount"
      @update:page="goToPage"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import AppointmentCard from "../../components/ui/AppointmentCard.vue";
import Pagination from "../../components/ui/Pagination.vue";
import { useAppointmentStore } from "../../stores/appointmentStore";
import LinkButton from "../../components/ui/LinkButton.vue";
const store = useAppointmentStore();
const currentPage = ref(1);
const sortOrder = ref("asc");

// Cargar reservas
const loadAppointments = async () => {
  await store.fetchAppointments(currentPage.value);
  sortAppointments();
};

const goToPage = (page) => {
  currentPage.value = page;
  loadAppointments();
};

// Cambiar estado
const updateStatus = async (id, status) => {
  await store.updateStatus(id, status);
  loadAppointments();
};

// Ordenar por fecha
const sortAppointments = () => {
  store.appointments.sort((a, b) => {
    return sortOrder.value === "asc"
      ? new Date(a.date) - new Date(b.date)
      : new Date(b.date) - new Date(a.date);
  });
};

const sortedAppointments = computed(() => store.appointments);

onMounted(loadAppointments);
</script>
