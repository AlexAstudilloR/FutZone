<script setup>
defineProps({
  message: {
    type: String,
    default: 'No hay datos para mostrar',
  },
})
</script>

<template>
  <div class="flex flex-col items-center justify-center text-center py-12 px-4">
    <img
      src="/nodata.webp"
      alt="Sin datos"
      class="w-40 h-40 object-contain mb-4 opacity-80"
    />
    <p class="text-gray-600 text-sm font-medium">
      {{ message }}
    </p>
  </div>
</template>