<template>
  <router-link :to="to" class="block">
    <div class="bg-white rounded-xl p-4 w-full cursor-pointer shadow-md hover:scale-105 transition transform border border-gray-200">
      <div class="flex items-center justify-center space-x-3">
        <font-awesome-icon :icon="['fas', icon]" :class="['text-2xl', iconColor]" />
        <h2 class="text-lg font-semibold text-gray-800">{{ title }}</h2>
      </div>
    </div>
  </router-link>
</template>

<script setup>
defineProps({
  title: String,
  icon: String,        // ← cambiado
  iconColor: String,
  to: {
    type: String,
    default: '/admin/appointments'
  }
})
</script>
