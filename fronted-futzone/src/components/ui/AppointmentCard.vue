<template>
  <div class="bg-white border rounded-lg p-4 shadow-sm flex justify-between items-center mb-4">
    <!-- Info de la reserva -->
    <div>
      <p><strong>Cliente:</strong> {{ appointment.user_name }}</p>
      <p><strong>Fecha:</strong> {{ appointment.date }}</p>
      <p><strong>Horario:</strong> {{ appointment.time_start }}–{{ appointment.time_end }}</p>
      <p><strong>Cancha:</strong> {{ appointment.field_name }}</p>
      <p><strong>Horas totales:</strong> {{ totalHours }}</p>
      <p><strong>Total:</strong> ${{ appointment.valor_pagar }}</p>
    </div>

    <!-- Botones -->
    <div class="flex flex-col gap-2">
      <button
        @click="$emit('accept')"
        class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
      >
        Aceptar
      </button>
      <button
        @click="$emit('reject')"
        class="border border-red-500 text-red-500 px-4 py-2 rounded hover:bg-red-100"
      >
        Rechazar
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  appointment: Object
})

const totalHours = computed(() => {
  const start = parseInt(props.appointment.time_start.split(':')[0])
  const end = parseInt(props.appointment.time_end.split(':')[0])
  return end - start
})
</script>
