<template>
  <div
    class="bg-white shadow-md rounded-xl p-4 w-full max-w-xs mx-auto text-center space-y-3"
  >
    <h2 class="text-lg font-semibold">{{ nombre }}</h2>

    <img
      src="/cancha.jpg"
      alt="Imagen de cancha"
      class="w-full h-48 object-cover rounded-md bg-gray-300"
    />

    <div class="text-sm">
      <p class="font-semibold">Tipo de cancha</p>
      <p>{{ tipo }}</p>
    </div>

    <div class="text-sm">
      <p class="font-semibold">Precio por hora</p>
      <p>${{ Number(precio).toFixed(2) }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  nombre: String,
  tipo: String,
  precio: Number,
});
</script>
