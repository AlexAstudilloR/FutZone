<template>
  <div class="p-6 space-y-6">
    <h1 class="text-2xl font-bold">Panel administrativo</h1>
    <p class="text-xl text-center">
      Bienvenido al panel administrativo de FutZone
    </p>

    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <DashboardCard
        title="Horarios"
        icon="clock"
        iconColor="text-red-500"
        to="/admin/schedules"
      />
      <DashboardCard
        title="Reservas"
        icon="calendar-check"
        iconColor="text-indigo-500"
        to="/admin/appointments"
      />
      <DashboardCard
        title="Canchas"
        icon="futbol"
        iconColor="text-green-500"
        to="/admin/fields"
      />
    </div>

    <div class="space-y-4">
      <h2 class="text-xl font-semibold">Estadísticas</h2>
      <p>Horario - hoy {{ summary?.period }}</p>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <AdminBlock title="Resumen de reservas diario" :items="reservaStats">
          <template #default="{ item }">
            <DashboardStatCard
              :title="item.title"
              :value="item.value"
              :icon="item.icon"
              :bgColor="item.bgColor"
              :textColor="item.textColor"
            />
          </template>
        </AdminBlock>

        <AdminBlock title="Resumen de actividad" :items="actividadStats">
          <template #default="{ item }">
            <DashboardStatCard
              :title="item.title"
              :value="item.value"
              :icon="item.icon"
              :bgColor="item.bgColor"
              :textColor="item.textColor"
            />
          </template>
        </AdminBlock>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from "vue";
import dayjs from "dayjs";
import DashboardCard from "../../components/admin/DashboardCard.vue";
import DashboardStatCard from "../../components/admin/StatCard.vue";
import AdminBlock from "../../components/admin/AdminBlock.vue";
import { useAppointmentStore } from "../../stores/appointmentStore";

const store = useAppointmentStore();
const today = dayjs().format("YYYY-MM-DD");

onMounted(() => {
  store.fetchDailySummary(today);
  store.fetchTimeSlots(today, null, 60);
});

const summary = computed(() => store.summary);

const reservaStats = computed(() => [
  {
    title: "Total",
    value: summary.value?.total_reservations ?? 0,
    icon: "calendar-check",
    bgColor: "bg-indigo-200",
    textColor: "text-indigo-800",
  },
  {
    title: "Rechazadas",
    value: summary.value?.status_breakdown?.rejected ?? 0,
    icon: "circle-xmark",
    bgColor: "bg-red-200",
    textColor: "text-red-800",
  },
  {
    title: "Aceptadas",
    value: summary.value?.status_breakdown?.accepted ?? 0,
    icon: "circle-check",
    bgColor: "bg-green-200",
    textColor: "text-green-800",
  },
  {
    title: "Por revisar",
    value: summary.value?.status_breakdown?.pending ?? 0,
    icon: "hourglass-half",
    bgColor: "bg-yellow-200",
    textColor: "text-yellow-800",
  },
]);

const actividadStats = computed(() => [
  {
    title: "Canchas ocupadas",
    value: summary.value?.total_reservations ?? 0,
    icon: "gauge-high",
    bgColor: "bg-indigo-200",
    textColor: "text-indigo-800",
  },
  {
    title: "Recaudado hoy",
    value: `$${summary.value?.total_income ?? "0.00"}`,
    icon: "dollar-sign",
    bgColor: "bg-green-200",
    textColor: "text-green-800",
  },
  {
    title: "Tiempo promedio",
    value: formatMinutes(summary.value?.average_duration_minutes ?? 0),
    icon: "clock",
    bgColor: "bg-gray-200",
    textColor: "text-gray-800",
  },
]);

const formatMinutes = (mins) => {
  const h = Math.floor(mins / 60);
  const m = Math.round(mins % 60);
  return h > 0 ? `${h}h ${m > 0 ? m + "min" : ""}` : `${m}min`;
};
</script>
