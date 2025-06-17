<template>
  <router-link :to="to" class="block">
    <div :class="['rounded-xl p-4 w-full cursor-pointer shadow-lg hover:opacity-90 transition hover:scale-105', bgColor]">
      <div class="flex  items-center justify-center space-x-2 ">
        <img :src="image" alt="icon" class="w-12 h-12" />
        <h2 class="text-white font-bold text-lg ">{{ title }}</h2>
      </div>
    </div>
  </router-link>
</template>

<script setup>
defineProps({
  title: String,
  image: String,
  bgColor: String,
  to: {
    type: String,
    default: '/admin/appointments'
  }
})
</script>
