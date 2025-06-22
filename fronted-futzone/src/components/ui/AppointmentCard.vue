<template>
  <div
    class="border rounded-lg p-4 shadow-sm mb-4 flex justify-between items-center transition"
    :class="{
      'bg-white':
        appointment.status === 'pending' || appointment.status === 'accepted',
      'bg-gray-100 opacity-80': appointment.status === 'rejected',
    }"
  >
    <div class="flex flex-col md:flex-row justify-between w-full gap-4">

      <div class="grid grid-cols-2 gap-y-1 text-sm flex-1">
        <p><strong>Cliente:</strong> {{ appointment.user_full_name }}</p>
        <p><strong>Fecha:</strong> {{ appointment.date }}</p>
        <p>
          <strong>Horario:</strong> {{ appointment.time_start }}–{{
            appointment.time_end
          }}
        </p>
        <p><strong>Cancha:</strong> {{ appointment.field_name }}</p>
        <p><strong>Horas:</strong> {{ totalHours }}</p>
        <p><strong>Total:</strong> ${{ appointment.valor_pagar }}</p>
      </div>

      <!-- Acciones o estado -->
      <div class="flex flex-col justify-center items-end min-w-[120px]">
        <div
          v-if="props.isAdmin && appointment.status === 'pending'"
          class="flex flex-col gap-2"
        >
          <button
            @click="$emit('accept')"
            class="bg-green-600 text-white px-3 py-1.5 rounded hover:bg-green-700 text-sm"
          >
            Aceptar
          </button>
          <button
            @click="$emit('reject')"
            class="border border-red-500 text-red-500 px-3 py-1.5 rounded hover:bg-red-100 text-sm"
          >
            Rechazar
          </button>
        </div>

        <p
          v-else
          class="text-sm font-semibold"
          :class="{
            'text-green-600': appointment.status === 'accepted',
            'text-red-500': appointment.status === 'rejected',
          }"
        >
          {{ estadoTexto }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  appointment: Object,
  isAdmin: {
    type: Boolean,
    default: false,
  },
});
const totalHours = computed(() => {
  const start = parseInt(props.appointment.time_start.split(":")[0]);
  const end = parseInt(props.appointment.time_end.split(":")[0]);
  return end - start;
});

const estadoTexto = computed(() => {
  if (props.appointment.status === "accepted") return "Aceptada";
  if (props.appointment.status === "rejected") return "Rechazada";
  return "Pendiente";
});
</script>
