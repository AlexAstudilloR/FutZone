<template>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <h3 class="text-lg font-semibold mb-2 ">Franjas Ocupadas</h3>
      <ul>
        <li v-for="(slot, index) in occupiedSlots" :key="`occ-${index}`" class="px-4 py-2 mb-2 bg-gray-200 rounded-lg text-red-600">
          {{ slot.start }} - {{ slot.end }}
        </li>
        <li v-if="!occupiedSlots.length" class="text-gray-500">No hay franjas ocupadas.</li>
      </ul>
    </div>

    <div>
      <h3 class="text-lg font-semibold mb-2 ">Franjas Disponibles</h3>
      <ul>
        <li v-for="(slot, index) in availableSlots" :key="`avail-${index}`" class="px-4 py-2 mb-2 rounded-lg text-green-600">
          {{ slot.start }} - {{ slot.end }}
        </li>
        <li v-if="!availableSlots.length" class="text-gray-500">No hay franjas disponibles.</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { onMounted, watch, computed } from 'vue'
import { useAppointmentStore } from '../../stores/appointmentStore.js'
import { defineProps } from 'vue'

const props = defineProps({
  fieldId: {
    type: [String, Number],
    required: true
  },
  date: {
    type: String,
    default: () => new Date().toISOString().slice(0, 10)
  },
  slotMinutes: {
    type: Number,
    default: 60
  }
})

const store = useAppointmentStore()

const occupiedSlots = computed(() => store.occupiedSlots)
const availableSlots = computed(() => store.availableSlots)

const loadSlots = () => {
  store.fetchTimeSlots(props.date, props.fieldId, props.slotMinutes)
}
onMounted(loadSlots)
watch(() => [props.date, props.fieldId, props.slotMinutes], loadSlots)
</script>
