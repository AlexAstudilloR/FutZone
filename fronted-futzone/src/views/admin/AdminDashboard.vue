<template>
  <div class="p-6 space-y-6">
    <h1 class="text-2xl font-bold">Panel administrativo</h1>
    <p class="text-lg">Bienvenido al panel administrativo de FutZone</p>

    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <DashboardCard
        title="Horarios"
        image="/horario-panel.svg"
        bgColor="bg-red-400"
        to="/admin/schedules"
      />
      <DashboardCard
        title="Reservas"
        image="/reserva-panel.svg"
        bgColor="bg-indigo-400"
        to="/admin/appointments"
      />
      <DashboardCard
        title="Canchas"
        image="/cancha-panel.svg"
        bgColor="bg-green-400"
        to="/admin/fields"
      />
    </div>

    <div class="space-y-4">
      <h2 class="text-xl font-semibold">Estadísticas</h2>
      <p>Horario - hoy {{ summary?.date }}</p>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <StatCard
          title="Reservas del día"
          :value="summary?.total_reservations ?? 0"
          bgColor="bg-indigo-200"
          textColor="text-indigo-800"
        />
        <StatCard
          title="Recaudado hoy"
          :value="`$${summary?.total_income ?? '0.00'}`"
          bgColor="bg-green-200"
          textColor="text-green-800"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import DashboardCard from "../../components/admin/DashboardCard.vue";
import StatCard from "../../components/admin/StatCard.vue";
import { useAppointmentStore } from "../../stores/appointmentStore";
import { onMounted, computed } from "vue";
import dayjs from "dayjs";

const store = useAppointmentStore();
const today = dayjs().format("YYYY-MM-DD");

onMounted(() => {
  store.fetchDailySummary(today);
});

const summary = computed(() => store.summary);
</script>
