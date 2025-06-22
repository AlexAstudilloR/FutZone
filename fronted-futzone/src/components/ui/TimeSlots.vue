<template>
  <div>
    <div
      class="flex justify-center items-center gap-6 mb-6 text-sm text-gray-700"
    >
      <div class="flex items-center gap-2">
        <span class="inline-block w-3 h-3 rounded-full bg-blue-500"></span>
        <span>Disponible</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="inline-block w-3 h-3 rounded-full bg-red-500"></span>
        <span>Reservado</span>
      </div>
    </div>

    <div
      v-if="props.fieldId && props.date"
      class="flex flex-wrap justify-center gap-3"
    >
      <div
        v-for="(slot, index) in allSlots"
        :key="`slot-${index}`"
        :class="[
          'w-[120px] h-[36px] flex items-center justify-center rounded-lg text-sm font-medium shadow-sm transition-all duration-200',
          slot.booked
            ? 'bg-red-100 text-red-700 cursor-not-allowed'
            : 'bg-blue-100 text-blue-700 hover:bg-blue-200 hover:scale-[1.03] active:scale-95 cursor-pointer',
        ]"
        @click="!slot.booked && emitSlotClick(slot.label)"
      >
        {{ slot.label }}
      </div>

      <p v-if="!allSlots.length" class="text-center mt-6 text-gray-500 w-full">
        No hay horarios disponibles.
      </p>
    </div>

   
    <div v-else class="text-center text-gray-500 mt-6">
      Selecciona una fecha y una cancha para ver los horarios disponibles.
    </div>
  </div>
</template>

<script setup>
import { onMounted, watch, computed } from "vue";
import { useAppointmentStore } from "../../stores/appointmentStore.js";

const props = defineProps({
  fieldId: {
    type: [String, Number],
    required: true,
  },
  date: {
    type: String,
    default: () => new Date().toISOString().slice(0, 10),
  },
  slotMinutes: {
    type: Number,
    default: 60,
  },
});

const store = useAppointmentStore();

const occupiedSlots = computed(() => store.occupiedSlots);
const availableSlots = computed(() => store.availableSlots);

const allSlots = computed(() => {
  const formatSlot = (slot, booked = false) => ({
    label: `${slot.start} - ${slot.end}`,
    booked,
  });

  const occupied = occupiedSlots.value.map((s) => formatSlot(s, true));
  const available = availableSlots.value.map((s) => formatSlot(s, false));

  return [...occupied, ...available].sort((a, b) => {
    return (
      new Date(`1970-01-01T${a.label.split(" - ")[0]}`) -
      new Date(`1970-01-01T${b.label.split(" - ")[0]}`)
    );
  });
});

const loadSlots = () => {
  store.fetchTimeSlots(props.date, props.fieldId, props.slotMinutes);
};
const emit = defineEmits(["slotSelected"]);

function emitSlotClick(label) {
  const [start, end] = label.split(" - ");
  emit("slotSelected", { start, end });
}
onMounted(loadSlots);
watch(() => [props.date, props.fieldId, props.slotMinutes], loadSlots);
</script>
