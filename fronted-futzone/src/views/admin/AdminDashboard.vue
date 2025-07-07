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
      <!-- Selector de modo y fecha -->
      <div
        class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
      >
        <div class="flex items-center gap-2 flex-wrap">
          <span class="font-semibold">Modo:</span>
          <button @click="mode = 'day'" :class="buttonClass('day')">Día</button>
          <button @click="mode = 'range'" :class="buttonClass('range')">
            Rango
          </button>
          <button @click="mode = 'month'" :class="buttonClass('month')">
            Mes
          </button>
        </div>

        <Datepicker
          v-model="selectedDate"
          :range="mode === 'range'"
          :month-picker="mode === 'month'"
          :enable-time-picker="false"
          locale="es"
          auto-apply
          format="yyyy-MM-dd"
          placeholder="Seleccionar fecha"
          class="max-w-xs"
        />
      </div>

      <div class="flex justify-between items-center">
        <h2 class="text-xl font-semibold">Estadísticas</h2>
        <BaseButton variant="success" icon="file-excel" @click="exportStats">
          Exportar reporte
        </BaseButton>
      </div>

      <p>Horario - {{ summary?.period ?? "..." }}</p>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <AdminBlock title="Resumen de reservas" :items="reservaStats">
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
import { onMounted, ref, watch, computed } from "vue";
import dayjs from "dayjs";
import Datepicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

import DashboardCard from "../../components/admin/DashboardCard.vue";
import DashboardStatCard from "../../components/admin/StatCard.vue";
import AdminBlock from "../../components/admin/AdminBlock.vue";
import BaseButton from "../../components/ui/BaseButton.vue";

import { useAppointmentStore } from "../../stores/appointmentStore";
const store = useAppointmentStore();

const mode = ref("day"); // 'day' | 'range' | 'month'
const selectedDate = ref(new Date()); // asegura el día actual real
let isExporting = false;

onMounted(() => {
  handleDateChange(selectedDate.value);
  const today = dayjs().format("YYYY-MM-DD");
  store.fetchTimeSlots(today, null, 60);
});

watch(selectedDate, async (val) => {
  if (!val) return;
  await handleDateChange(val);
});

const handleDateChange = async (val) => {
  if (!val) return;

  if (mode.value === "range" && Array.isArray(val) && val.length === 2) {
    const [start, end] = val.map((d) => dayjs(d).format("YYYY-MM-DD"));
    await store.fetchSummary({ start_date: start, end_date: end });
  } else if (mode.value === "day") {
    const date = dayjs(val).format("YYYY-MM-DD");
    await store.fetchSummary({ date });
  } else if (mode.value === "month") {
    const { year, month } = val;
    if (typeof month !== "number" || typeof year !== "number") return;

    const realMonth = String(month + 1).padStart(2, "0");
    const realDate = dayjs(`${year}-${realMonth}-01`);
    if (!realDate.isValid()) return;

    const firstDay = realDate.startOf("month").format("YYYY-MM-DD");
    const lastDay = realDate.endOf("month").format("YYYY-MM-DD");

    await store.fetchSummary({ start_date: firstDay, end_date: lastDay });
  }
};

const buttonClass = (btnMode) =>
  `px-2 py-1 rounded border text-sm ${
    mode.value === btnMode
      ? "bg-indigo-500 text-white"
      : "bg-white text-gray-700"
  }`;

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
    title: "Cancha más usada",
    value: summary.value?.most_reserved_field ?? "Ninguna",
    icon: "gauge-high",
    bgColor: "bg-indigo-200",
    textColor: "text-indigo-800",
  },
  {
    title: "Recaudado",
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

const exportStats = async () => {
  if (isExporting) return;
  isExporting = true;

  try {
    let params = {};
    const val = selectedDate.value;

    if (mode.value === "range" && Array.isArray(val) && val.length === 2) {
      const [start, end] = val.map((d) => dayjs(d).format("YYYY-MM-DD"));
      params = { start_date: start, end_date: end };
    } else if (mode.value === "day") {
      params = { date: dayjs(val).format("YYYY-MM-DD") };
    } else if (mode.value === "month") {
      const { year, month } = val;
      if (typeof month === "number" && typeof year === "number") {
        const realDate = dayjs(
          `${year}-${String(month + 1).padStart(2, "0")}-01`
        );
        if (realDate.isValid()) {
          params = {
            start_date: realDate.startOf("month").format("YYYY-MM-DD"),
            end_date: realDate.endOf("month").format("YYYY-MM-DD"),
          };
        }
      }
    }

    await store.exportReservationsExcel(params);
  } catch (err) {
    console.error("Error al exportar Excel:", err);
  } finally {
    isExporting = false;
  }
};
</script>
