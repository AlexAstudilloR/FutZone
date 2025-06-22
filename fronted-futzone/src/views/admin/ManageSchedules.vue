<template>
  <div class="space-y-12 p-6">
    <div class="flex justify-between">
      <h2 class=" font-bold text-2xl">Gestión de horarios</h2>
      <LinkButton
        to="/admin"
        label="Volver a panel"
        :icon="['fas','arrow-left']"
        size="md"
        variant="none"
        color="inherit"
        extraClass="border border-[#19296D] text-[#19296D]
          hover:bg-[#19296D] hover:text-white transition-colors duration-200
          w-full sm:w-auto text-center"
      />
    </div>

    <CrudSection
      title="Horarios Semanales"
      singular="Horario"
      :items="scheduleStore.weekly"
      :fields="weeklyFields"
      :columns="weeklyColumns"
      :fetch-fn="scheduleStore.fetchWeekly"
      :create-fn="scheduleStore.createWeekly"
      :update-fn="scheduleStore.updateWeekly"
      :delete-fn="scheduleStore.deleteWeekly"
    />

    <CrudSection
      title="Excepciones Puntuales"
      singular="Excepción"
      :items="scheduleStore.exceptions"
      :fields="exceptionFields"
      :columns="exceptionColumns"
      :fetch-fn="scheduleStore.fetchExceptions"
      :create-fn="scheduleStore.createException"
      :update-fn="scheduleStore.updateException"
      :delete-fn="scheduleStore.deleteException"
    />
  </div>
</template>
<script setup>
import { onMounted, computed , watch} from "vue";
import { useScheduleStore } from "../../stores/scheduleStore";
import { useFieldStore } from "../../stores/fieldStore";
import CrudSection from "../../components/schedules/CrudSection.vue";
import LinkButton from "../../components/ui/LinkButton.vue";


const scheduleStore = useScheduleStore();
const fieldStore = useFieldStore();

const weeklyColumns = [
  { key: "cancha", label: "Cancha" },
  { key: "dia_display", label: "Día" },
  { key: "hora_apertura", label: "Apertura" },
  { key: "hora_cierre", label: "Cierre" },
];

const exceptionColumns = [
  { key: "cancha", label: "Cancha" },
  { key: "fecha", label: "Fecha" },
  { key: "hora_apertura", label: "Apertura" },
  { key: "hora_cierre", label: "Cierre" },
  { key: "cerrado_display", label: "Cerrado" },
  { key: "motivo", label: "Motivo" },
];

const weeklyFields = computed(() => [
  {
    prop: "cancha_id",
    label: "Cancha",
    type: "select",
    options: fieldStore.fields.map((f) => ({ value: f.id, label: f.name })),
  },
  {
    prop: "dia",
    label: "Día",
    type: "select",
    options: scheduleStore.diasChoices,
  },
  { prop: "hora_apertura", type: "time", label: "Apertura" },
  { prop: "hora_cierre", type: "time", label: "Cierre" },
]);

const exceptionFields = computed(() => [
  {
    prop: "cancha_id",
    label: "Cancha",
    type: "select",
    options: fieldStore.fields.map((f) => ({ value: f.id, label: f.name })),
  },
  { prop: "fecha", type: "date", label: "Fecha" },
  { prop: "hora_apertura", type: "time", label: "Apertura" },
  { prop: "hora_cierre", type: "time", label: "Cierre" },
  { prop: "cerrado", type: "checkbox", label: "Cerrado" },
  { prop: "motivo", type: "text", label: "Motivo" },
]);

onMounted(async () => {
  await fieldStore.fetchFields({ available: true });
  await scheduleStore.fetchDiasChoices();
  await scheduleStore.fetchWeekly();
  await scheduleStore.fetchExceptions();
});

</script>
