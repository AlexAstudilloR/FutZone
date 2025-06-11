<template>
  <div class="space-y-12 p-6">

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
import { onMounted, computed } from 'vue'
import { useScheduleStore } from '../../stores/scheduleStore'
import { useFieldStore } from '../../stores/fieldStore'
import CrudSection from '../../components/schedules/CrudSection.vue'

const scheduleStore = useScheduleStore()
const fieldStore    = useFieldStore()

// Campos/columnas semanales
const weeklyColumns = [
  { key: 'cancha',      label: 'Cancha' },
  { key: 'dia_display', label: 'Día' },
  { key: 'hora_apertura', label: 'Apertura' },
  { key: 'hora_cierre',   label: 'Cierre' },
  { key: 'cerrado',     label: 'Cerrado' },
]

// Campos/columnas excepciones
const exceptionColumns = [
  { key: 'cancha',      label: 'Cancha' },
  { key: 'fecha',       label: 'Fecha' },
  { key: 'hora_apertura', label: 'Apertura' },
  { key: 'hora_cierre',   label: 'Cierre' },
  { key: 'cerrado',     label: 'Cerrado' },
  { key: 'motivo',      label: 'Motivo' },
]

// Definimos los fields como *computed*, para que recojan automáticamente
// las opciones cuando lleguen los datos a los stores.
const weeklyFields = computed(() => [
  {
    prop: 'cancha',
    label: 'Cancha',
    options: fieldStore.fields,       // <— select de canchas
  },
  {
    prop: 'dia',
    label: 'Día',
    options: scheduleStore.diasChoices, // <— select de días
  },
  { prop: 'hora_apertura', label: 'Apertura', type: 'time' },
  { prop: 'hora_cierre',   label: 'Cierre',   type: 'time' },
  { prop: 'cerrado',      label: 'Cerrado',   type: 'checkbox' },
])

const exceptionFields = computed(() => [
  {
    prop: 'cancha',
    label: 'Cancha',
    options: fieldStore.fields,
  },
  { prop: 'fecha',        label: 'Fecha',     type: 'date' },
  { prop: 'hora_apertura', label: 'Apertura',  type: 'time' },
  { prop: 'hora_cierre',   label: 'Cierre',    type: 'time' },
  { prop: 'cerrado',      label: 'Cerrado',    type: 'checkbox' },
  { prop: 'motivo',       label: 'Motivo',    type: 'text' },
])

onMounted(async () => {

  await fieldStore.fetchFields({ available: true })


  await scheduleStore.fetchDiasChoices()


  scheduleStore.fetchWeekly()
  scheduleStore.fetchExceptions()
})
</script>

<style scoped>

</style>
