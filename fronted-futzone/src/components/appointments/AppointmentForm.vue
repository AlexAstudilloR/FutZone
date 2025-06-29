<script setup>
import { ref, watch, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useFieldStore } from "../../stores/fieldStore";

import BaseInput from "../ui/BaseInput.vue";
import BaseSelect from "../ui/BaseSelect.vue";

const props = defineProps({
  preselectedField: Object,
  preselectedSlot: Object,
});

const fieldStore = useFieldStore();
const route = useRoute();

const today = new Date().toISOString().split("T")[0];
const minDate = today;

const form = ref({
  date: today,
  field: null,
  time_start: "",
  time_end: "",
});

const isFieldPreselected = computed(() => !!route.query.fieldId || !!props.preselectedField);

const fieldOptions = computed(() =>
  fieldStore.fields.map((f) => ({ value: f.id, label: f.name }))
);

const selectedFieldName = computed(() => {
  const field = fieldStore.fields.find((f) => f.id === form.value.field);
  return field?.name || "";
});

onMounted(async () => {
  await fieldStore.fetchFields({ available: true });

  const preselectedId = props.preselectedField?.id || parseInt(route.query.fieldId);
  if (preselectedId) {
    const exists = fieldStore.fields.some((f) => f.id === preselectedId);
    if (exists) {
      form.value.field = preselectedId;
    }
  }
});

watch(
  () => props.preselectedSlot,
  (slot) => {
    if (slot && slot.start && slot.end) {
      form.value.time_start = slot.start;
      form.value.time_end = slot.end;
    }
  },
  { immediate: true, deep: true }
);

// Expone los datos del formulario al padre
defineExpose({
  getFormData: () => ({
    date: form.value.date,
    field: form.value.field,
    time_start: form.value.time_start,
    time_end: form.value.time_end,
  }),
});
</script>

<template>
  <div class="space-y-4 w-full">
    <h2 class="text-xl font-bold mb-2">
      Reservar Cancha
      <span class="block text-blue-700 font-light text-lg">{{ selectedFieldName }}</span>
    </h2>

    <div>
      <label class="block text-sm font-medium mb-1">Fecha de reserva</label>
      <BaseInput
        v-model="form.date"
        type="date"
        :min="minDate"
        required
      />
    </div>

    <div>
      <BaseSelect
        v-model="form.field"
        :options="fieldOptions"
        label="Cancha"
        placeholder="Selecciona una cancha"
        :disabled="isFieldPreselected"
        required
      />
    </div>

    <div class="grid grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium mb-1">Hora inicio</label>
        <BaseInput v-model="form.time_start" type="time" required />
      </div>
      <div>
        <label class="block text-sm font-medium mb-1">Hora fin</label>
        <BaseInput v-model="form.time_end" type="time" required />
      </div>
    </div>
  </div>
</template>
