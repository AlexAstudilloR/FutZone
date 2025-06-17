<template>
  <div class="max-w-4xl mx-auto p-6 bg-white shadow rounded-lg grid grid-cols-1 md:grid-cols-2 gap-8">
    <div>
      <h2 class="text-2xl font-bold mb-4">Reservar Cancha</h2>
      <form @submit.prevent="submit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">Fecha de reserva</label>
          <BaseInput
            v-model="form.date"
            type="date"
            :class="{ 'border-red-500': errors.date }"
            required
          />
          <p v-if="errors.date" class="text-red-500 text-sm mt-1">{{ errors.date[0] }}</p>
        </div>

        <div>
          <BaseSelect
            v-model="form.field"
            :options="fieldOptions"
            label="Cancha"
            placeholder="Selecciona una cancha"
            :class="{ 'border-red-500': errors.field }"
            required
          />
          <p v-if="errors.field" class="text-red-500 text-sm mt-1">{{ errors.field[0] }}</p>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium mb-1">Hora inicio</label>
            <BaseInput
              v-model="form.time_start"
              type="time"
              :class="{ 'border-red-500': errors.time_start }"
              required
            />
            <p v-if="errors.time_start" class="text-red-500 text-sm mt-1">{{ errors.time_start[0] }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Hora fin</label>
            <BaseInput
              v-model="form.time_end"
              type="time"
              :class="{ 'border-red-500': errors.time_end }"
              required
            />
            <p v-if="errors.time_end" class="text-red-500 text-sm mt-1">{{ errors.time_end[0] }}</p>
          </div>
        </div>

        <p v-if="errors.non_field_errors" class="text-red-500 text-sm">{{ errors.non_field_errors[0] }}</p>

        <div class="text-right">
          <BaseButton type="submit" variant="primary">Reservar</BaseButton>
        </div>
      </form>
    </div>


    <div>
      <TimeSlots
        v-if="form.field && form.date"
        :field-id="form.field"
        :date="form.date"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAppointmentStore } from '../../stores/appointmentStore'
import { useFieldStore } from '../../stores/fieldStore'
import BaseInput from '../../components/ui/BaseInput.vue'
import BaseSelect from '../../components/ui/BaseSelect.vue'
import BaseButton from '../../components/ui/BaseButton.vue'
import TimeSlots from '../../components/ui/TimeSlots.vue'

const appointmentStore = useAppointmentStore()
const fieldStore = useFieldStore()

const form = ref({ date: '', field: null, time_start: '', time_end: '' })
const errors = ref({})

onMounted(async () => {
  await fieldStore.fetchFields({ available: true })
})

const fieldOptions = computed(() =>
  fieldStore.fields.map(f => ({ value: f.id, label: f.name }))
)

async function submit() {
  errors.value = {}
  try {
    await appointmentStore.createAppointment({
      date: form.value.date,
      field: form.value.field,
      time_start: form.value.time_start,
      time_end: form.value.time_end
    })
    form.value = { date: '', field: null, time_start: '', time_end: '' }
    alert('Reserva creada correctamente')
  } catch (err) {
    errors.value = err.response?.data || {}
  }
}
</script>

<style scoped>
</style>
