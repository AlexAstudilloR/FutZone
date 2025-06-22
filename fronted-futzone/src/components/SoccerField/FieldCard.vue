<template>
  <div
    class="bg-gradient-to-br from-white to-gray-50 border border-gray-200 shadow-lg hover:shadow-2xl rounded-2xl p-5 w-full max-w-xs mx-auto text-center space-y-4 transition-all duration-300 ease-in-out"
  >
    <h2 class="text-xl font-bold text-gray-800 tracking-wide">{{ nombre }}</h2>

    <img
      :src="imageUrl"
      :alt="`Imagen de ${nombre}`"
      class="w-full h-48 object-cover rounded-lg bg-gray-200 border"
      @error="handleImageError"
    />

    <div class="text-sm text-gray-600">
      <p class="font-semibold text-gray-500 uppercase">Tipo de cancha</p>
      <p>{{ tipo }}</p>
    </div>

    <div class="text-sm text-gray-600">
      <p class="font-semibold text-gray-500 uppercase">Precio por hora</p>
      <p class="text-green-600 font-bold">${{ precioNumerico.toFixed(2) }}</p>
    </div>

    <button
      class="mt-2 w-full bg-green-500 hover:bg-green-800 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300"
      @click="abrirReserva"
    >
      Reservar
    </button>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";

const props = defineProps({
  id: [Number, String], // ✅ necesario para redirección
  nombre: String,
  tipo: String,
  precio: [Number, String],
  imagen: String,
});

const emit = defineEmits(["reservar"]);

const imageError = ref(false);

const precioNumerico = computed(() => {
  return typeof props.precio === "string"
    ? parseFloat(props.precio)
    : props.precio;
});

const imageUrl = computed(() => {
  if (imageError.value || !props.imagen) {
    return "/cancha.jpg";
  }

  if (props.imagen.startsWith("http")) {
    return props.imagen;
  }

  const baseURL = import.meta.env.VITE_BASE_URL || "http://localhost:8000";
  const imagePath = props.imagen.startsWith("/media")
    ? props.imagen
    : `/media/${props.imagen}`;
  return `${baseURL}${imagePath}`;
});

function handleImageError() {
  imageError.value = true;
}

function abrirReserva() {
  emit("reservar", {
    id: props.id, // ✅ esto es lo que faltaba
    nombre: props.nombre,
    tipo: props.tipo,
    precio: precioNumerico.value,
    imagen: imageUrl.value,
  });
}
</script>
